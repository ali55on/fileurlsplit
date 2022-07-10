#!/usr/bin/env python3
import os
import re
import string
import sys
import urllib.parse


class Error(Exception):
    """Exception base class"""
    pass


class FilenameTooLongError(Error):
    """Raised when the file name is too long.
    Usually longer than 255 characters.
    """
    pass


class AbsolutePathError(Error):
    """Raised when a passed URL doesn't have an absolute path
    prefix like a slash "/" or "file://".
    """
    pass


class InvalidCharacterError(Error):
    """Raised when the string contains a character not allowed
    for the desired action.
    """
    pass


class ValidWindowsFilename(object):
    def __init__(self, filename: str):
        self.__filename = filename
        self.__all_invalid_strings = self.__get_all_invalid_strings()
        self.__is_valid_filename = self.__get_is_valid_filename()
        self.__warning_msg = None
        self.__invalid_string_found = None

    def __get_is_valid_filename(self) -> bool:
        # 'starts-with'
        for invalid_item in self.__all_invalid_strings['starts-with']:
            if self.__filename.startswith(invalid_item):
                self.__warning_msg = f"cannot start with '{invalid_item}'"
                self.__invalid_string_found = invalid_item
                return False

        # 'any-position'
        for invalid_item in self.__all_invalid_strings['any-position']:
            if invalid_item in self.__filename:
                self.__warning_msg = f"Cannot contain '{invalid_item}'"
                self.__invalid_string_found = invalid_item
                return False

        return True

    @staticmethod
    def __get_all_invalid_strings() -> dict:
        return {
            'starts-with': ['0x00', '0xFF', '0xE5'],
            'any-position': [
                # chars
                '"', '*', '/', ':', '<', '>', '?', '\\', '|', '+', ',',
                '.', ';', '=', '[', ']', '!', '@',
                # hex unit
                '0x0', '0x1', '0x2', '0x3', '0x4', '0x5', '0x6', '0x7', '0x8',
                '0x9', '0xa', '0xb', '0xc', '0xd', '0xe', '0xf',
                # hex 0_unit
                '0x00', '0x01', '0x02', '0x03', '0x04', '0x05', '0x06', '0x07',
                '0x08', '0x09', '0x0a', '0x0b', '0x0c', '0x0d', '0x0e', '0x0f',
                # hex ten
                '0x10', '0x11', '0x12', '0x13', '0x14', '0x15', '0x16', '0x17',
                '0x18', '0x19', '0x1a', '0x1b', '0x1c', '0x1d', '0x1e', '0x1f',
                # hex unit: upper
                '0xA', '0xB', '0xC', '0xD', '0xE', '0xF',
                # hex 0_unit: upper
                '0x0A', '0x0B', '0x0C', '0x0D', '0x0E', '0x0F',
                # hex ten: upper
                '0x1A', '0x1B', '0x1C', '0x1D', '0x1E', '0x1F',
                # hex ++
                '0x7F', '0x7f']}


class ValidWindowsPath(object):
    def __init__(self, path: str):
        self.__path = path
        self.__all_invalid_strings = self.__get_all_invalid_strings()
        self.__is_valid_path = self.__get_is_valid_path()
        self.__warning_msg = None
        self.__invalid_string_found = None

    def __get_is_valid_path(self) -> bool:
        # 'reserved-paths'
        for invalid_item in self.__all_invalid_strings['reserved-paths']:
            if invalid_item in self.__path:
                self.__warning_msg = f"Cannot contain '{invalid_item}'"
                self.__invalid_string_found = invalid_item
                return False

        # 'reserved-directory-names'
        for reserved_dir in self.__all_invalid_strings[
                'reserved-directory-names']:
            for path_dir in self.__path.split('/'):
                if path_dir == reserved_dir:
                    self.__warning_msg = f"Cannot contain '{reserved_dir}'"
                    self.__invalid_string_found = reserved_dir
                    return False

        return True

    @staticmethod
    def __get_all_invalid_strings() -> dict:
        return {
            'reserved-paths': [
                '$Extend/$ObjId', '$Extend/$Quota', '$Extend/$Reparse'],
            'reserved-directory-names': [
                '$Quota', '$ObjId', '$Reparse',
                # devices
                '$', '$IDLE$', 'AUX', 'COM1', 'COM2', 'COM3', 'COM4',
                'CON', 'CONFIG$', 'CLOCK$', 'KEYBD$', 'LPT1', 'LPT2',
                'LPT3', 'LPT4', 'LST', 'NUL', 'PRN', 'SCREEN$',
                # root
                '$AttrDef', '$BadClus', '$Bitmap', '$Boot', '$LogFile',
                '$MFT', '$MFTMirr', 'pagefile.sys', '$Secure', '$UpCase',
                '$Volume', '$Extend']}


class ValidName(object):
    def __init__(self):
        self.__platform = self.__get_platform()
        self.__safe_valid_chars = list(
            string.ascii_letters + string.digits + '~ -_.')

    @staticmethod
    def __get_platform() -> str:
        if sys.platform.startswith('linux'):
            return 'linux'
        elif 'bsd' in sys.platform:
            return 'bsd'
        elif 'darwin' in sys.platform:
            return 'mac'
        elif 'win' in sys.platform or 'msys' in sys.platform:
            return 'windows'
        else:
            return 'other'


class FileUrlSplit(object):
    """Object that handles file url divisions

    From the file you can get the full url, extension, name or path.

    Use '/path', 'c:\\path', or 'file:///path'
    >>> file_url_split = FileUrlSplit(file_url='file:///home/user/photo.png')

    >>> print(file_url_split)
    FileUrlSplit("/home/user/photo.png")

    Get url
    >>> file_url_split.url
    '/home/user/photo.png'

    Get only file path
    >>> file_url_split.path
    '/home/user/'

    Get only file name without the extension
    >>> file_url_split.name
    'photo'

    Get filename with the extension
    >>> file_url_split.filename
    'photo.png'

    Get file extension
    >>> file_url_split.extension
    '.png'
    """

    def __init__(self, file_url: str) -> None:
        """Constructor

        It will not be checked if the file from the passed URL already exists.
        The goal is just to split the string.

        The URL must be absolute or an exception will be raised. This means
        that the string must start with a valid path prefix. Example: '/path',
        'c:/path', 'file:///path'.

        If the URL contains backslashes '\', then it must be escaped or passed
        as a raw string. Example: r'C:\path', 'c:\\path'

        :param file_url: URL string
        """
        self.__url = self.__get_url(file_url)
        self.__path = self.__get_path()
        self.__filename = self.__get_filename()
        self.__extension = self.__get_extension()
        self.__name = self.__get_name()

    @property
    def url(self) -> str:
        """Get the clean url

        URL without the file prefix, such as "file://".

        :return: File url
        """
        return self.__url

    @url.setter
    def url(self, file_url: str) -> None:
        """Set up a new URL

        A new URL can change all other properties.
        The URL must be absolute or an exception will be raised.
        This means that the string must start with a valid path prefix.
        Example: '/path', 'c:/path', 'file:///path'.

        :param file_url: New URL string
        """
        if file_url != self.__url:
            self.__url = self.__get_url(file_url)
            self.__path = self.__get_path()
            self.__filename = self.__get_filename()
            self.__extension = self.__get_extension()
            self.__name = self.__get_name()

    @property
    def path(self) -> str:
        """Get file path only

        The path without the file name and extension.

        :return: File path
        """
        return self.__path

    @path.setter
    def path(self, file_path: str) -> None:
        """Set a new path to the file

        The path must have absolute URL or an exception will be raised.
        This means that the string must start with a valid path prefix.
        Example: '/path', 'c:/path', 'file:///path'.
        This also updates the 'url' propertie.

        :param file_path: New path URL string
        """
        if file_path != self.__path:
            if file_path[-1] != '/':
                file_path = file_path + '/'

            self.__url = self.__get_url(file_path + self.__filename)
            self.__path = self.__get_path()

    @property
    def name(self) -> str:
        """Get only the file name

        File name without the extension and without the path.

        :return: File name
        """
        return self.__name

    @name.setter
    def name(self, file_name: str) -> None:
        """Set a new name for the file

        This also updates the 'url' and 'filename' properties.
        The extension doesn't change, so just pass the filename without the
        extension.
        If you want to pass a name along with the extension and change
        everything at once, use the "filename" property of this class.
        If you only want to change the file extension, use the "extension"
        property.

        :param file_name: String containing the file name
        """
        if file_name != self.__name:
            if '/' in file_name or '\\' in file_name:
                raise InvalidCharacterError(
                    'It must be just the name. The name is not part of a full '
                    "URL, so it cannot contain slashes '/'")

            if len(file_name + self.__extension) > 255:
                raise FilenameTooLongError(
                    'Very big name. '
                    'The size limit for filenames is 255 characters.')

            self.__name = file_name
            self.__filename = self.__name + self.__extension
            self.__url = self.__path + self.__filename

    @property
    def filename(self) -> str:
        """Get only the filename

        Filename with the extension but without the path.

        :return: Filename
        """
        return self.__filename

    @filename.setter
    def filename(self, filename: str) -> None:
        """Set a new filename for the file

        This also updates the 'url', 'name' and 'extension' properties.
        It must contain the file extension, such as "foo.txt". If you don't
        pass the name along with the extension, then the existing extension
        will be removed.
        If you want to change the name of the file without changing the
        existing extension, use the "name" property of this class.

        :param filename: String containing the filename
        """
        if filename != self.__filename:
            if '/' in filename or '\\' in filename:
                raise InvalidCharacterError(
                    'It must be just the filename. '
                    'The filename is not part of a full URL, '
                    "so it cannot contain slashes '/'")

            if len(filename) > 255:
                raise FilenameTooLongError(
                    'Very big name. '
                    'The size limit for filenames is 255 characters.')

            self.__filename = filename
            self.__url = self.__path + self.__filename
            self.__extension = self.__get_extension()
            self.__name = self.__get_name()

    @property
    def extension(self) -> str:
        """Get file extension only

        Only the file extension without the name and path.

        :return: File extension
        """
        return self.__extension

    @extension.setter
    def extension(self, file_extension: str) -> None:
        """Set a new extension for the file

        This also updates the 'url', and 'filename'properties.

        :param file_extension: String containing the filename extension
        """
        if file_extension != self.__extension:
            if '/' in file_extension or '\\' in file_extension:
                raise InvalidCharacterError(
                    'It must be just the filename. '
                    'The filename is not part of a full URL, '
                    "so it cannot contain slashes '/'")

            if file_extension[0] != '.':
                file_extension = '.' + file_extension

            if len(self.__name + file_extension) > 255:
                raise FilenameTooLongError(
                    'Very big name. '
                    'The size limit for filenames is 255 characters.')

            self.__extension = file_extension
            self.__url = self.__path + self.__name + self.__extension
            self.__filename = self.__get_filename()

    @staticmethod
    def __get_url(file_url: str) -> str:
        # Returns a clean url
        # Decode url-encode and remove prefix like "file://", "c:/"

        # Fix slash
        file_url = file_url.replace('\\', '/')

        # Raise a non-absolute path
        absolute_path_error_msg = (
            'You need an absolute URL like: '
            '"/path", "file://path", "file:///path" or "c:/path"')
        prefix_match = re.search(r'^\w+:', file_url)  # file prefix -> c: file:
        if prefix_match:
            if file_url[prefix_match.end():][0] != '/':
                raise AbsolutePathError(absolute_path_error_msg)
        else:
            if file_url[0] != '/':
                raise AbsolutePathError(absolute_path_error_msg)

        # Match - remove prefix like "file://", "c:/"
        match = re.search(r'/\w.+$', file_url)

        # Decode url
        return urllib.parse.unquote(
            string=file_url[match.start():match.end()],
            encoding='utf-8',
            errors='replace')

    def __get_path(self) -> str:
        # Returns only the file path
        path = os.path.dirname(self.__url)
        return path if path == '/' else path + '/'

    def __get_filename(self) -> str:
        # Returns the filename with the extension
        return self.__url.replace(self.__path, '')

    def __get_extension(self):
        # Returns only the file extension

        # splitext does not work for .tar*
        # >>> filename, file_extension = os.path.splitext("/path/foo.tar.gz")
        # >>> file_extension
        # '.gz'

        # Olhar o fim do nome do arquivo a partir do último ponto, não produz
        # o resultado esperado, pois um arquivo de nome '.txt' não pode ser
        # reconhecido como um arquivo de nome vazio '' e extensão '.txt', e
        # sim como um arquivo que tem o nome oculto '.txt' e extensão vazia ''.
        # Remover o ponto '.' no início do nome do arquivo, ajuda na posterior
        # divisão ( split('.') ). Na extensão nada é alterado.
        file_name = self.__filename.lstrip('.')

        # Arquivos sem extensão
        if '.' not in file_name or file_name[-1] == '.':
            return ''

        # Divide o nome do arquivo em todos os pontos, criando uma lista.
        # O último item, representam a extensão.
        file_slices = file_name.split('.')

        # Pontos no início e fim ja foram tratados, então uma lista de 2 itens
        # representa um arquivo que só tem uma extensão.
        # O primeiro item é o nome do arquivo, e último item é a extensão.
        if len(file_slices) == 2:
            return '.' + file_slices[-1]

        # Lista sempre de 3 itens pra cima, representa arquivo que
        # tem mais de uma extensão, ou pontos no meio do nome.
        elif len(file_slices) > 2:

            # Extensão interna. Futuramente, adicionar extensões internas aqui.
            if file_slices[-2] == 'tar':
                return '.' + file_slices[-2] + '.' + file_slices[-1]

            return '.' + file_slices[-1]

    def __get_name(self) -> str:
        # Returns the file name without the extension
        return self.__filename.replace(self.__extension, '')

    def __repr__(self):
        return f'FileUrlSplit("{self.__url}")'


if __name__ == "__main__":
    # No third-party testing coverage
    import doctest     # pragma: no cover
    doctest.testmod()  # pragma: no cover
