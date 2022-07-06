#!/usr/bin/env python3
import os
import re
import urllib.parse


class FileUrlSplit(object):
    """Object that handles file url divisions

    From the file you can get the full url, extension, name or path.
    Use '/path', 'c:\\path', or 'file:///path'

    >>> file_url_split = FileUrlSplit(file_url='file:///home/user/photo.png')

    >>> print(file_url_split)
    <FileUrlSplit '/home/user/photo.png'>

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

        :param file_url:
        """
        self.__url = self.__get_url(file_url)
        self.__path = self.__get_path()
        self.__filename = self.__get_filename()
        self.__extension = self.__get_extension()
        self.__name = self.__get_name()

    @property
    def url(self) -> str:
        return self.__url

    @property
    def path(self) -> str:
        return self.__path

    @property
    def name(self) -> str:
        return self.__name

    @property
    def filename(self) -> str:
        return self.__filename

    @property
    def extension(self) -> str:
        return self.__extension

    @staticmethod
    def __get_url(file_url: str) -> str:
        # Returns a clean url
        # Decode url-encode and remove prefix like "file://", "c:/"

        # Fix slash
        file_url = file_url.replace('\\', '/')
        if file_url.lower()[:2] != 'c:' and file_url.lower()[:5] != 'file:':
            if file_url[0] != '/':
                raise ValueError(
                    'You need an absolute URL like: '
                    '"/path", "file://path", "file:///path" or "c:/path"')

        # Match - remove prefix like "file://", "c:/"
        match = re.search(r'/\w.+$', file_url)

        # Decode url
        return urllib.parse.unquote(
            string=file_url[match.start():match.end()],
            encoding='utf-8',
            errors='replace')

    def __get_path(self) -> str:
        # Returns only the file path
        return os.path.dirname(self.__url) + '/'

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
        return f"<FileUrlSplit '{self.__url}'>"


if __name__ == "__main__":
    import doctest
    doctest.testmod()
