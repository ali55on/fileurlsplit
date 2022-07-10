#!/usr/bin/env python3
import os
import re
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
