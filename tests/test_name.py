#!/usr/bin/env python3
import unittest

import src.fileurlsplit as file_url_split


class TestNameProperty(unittest.TestCase):

    def test_name(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        self.assertEqual(file_url.name, 'text')

    def test_name_with_space(self):
        file_url = file_url_split.FileUrlSplit('/home/user/the text.txt')
        self.assertEqual(file_url.name, 'the text')

    def test_name_without_extension(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text')
        self.assertEqual(file_url.name, 'text')

    def test_hidden_file_name(self):
        file_url = file_url_split.FileUrlSplit('/home/user/.the text.txt')
        self.assertEqual(file_url.name, '.the text')

    def test_hidden_file_name_without_extension(self):
        file_url = file_url_split.FileUrlSplit('/home/user/.text')
        self.assertEqual(file_url.name, '.text')


class TestNameSetter(unittest.TestCase):

    def test_new_name(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        file_url.name = 'foo'
        self.assertEqual(file_url.name, 'foo')
        self.assertEqual(file_url.url, '/home/user/foo.txt')
        self.assertEqual(file_url.filename, 'foo.txt')

    def test_remove_name(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        file_url.name = ''
        self.assertEqual(file_url.url, '/home/user/.txt')
        self.assertEqual(file_url.path, '/home/user/')
        self.assertEqual(file_url.name, '.txt')
        self.assertEqual(file_url.filename, '.txt')

    def test_remove_name_without_extension(self):
        file_url = file_url_split.FileUrlSplit('/home/user/file')
        file_url.name = ''
        self.assertEqual(file_url.url, '/home/user/')
        self.assertEqual(file_url.path, '/home/user/')
        self.assertEqual(file_url.name, '')
        self.assertEqual(file_url.filename, '')


class TestNameRaises(unittest.TestCase):

    def test_new_name_raises(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        self.assertRaises(
            file_url_split.InvalidCharacterError,
            setattr, file_url, 'name', '/foo')

    def test_very_big_new_name_raises(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        new_name = 'A' * 256
        self.assertRaises(
            file_url_split.FilenameTooLongError,
            setattr, file_url, 'name', new_name)


if __name__ == '__main__':
    # No third-party testing coverage
    unittest.main()  # pragma: no cover
