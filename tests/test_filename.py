#!/usr/bin/env python3
import unittest

import src.fileurlsplit as file_url_split


class TestFilenameProperty(unittest.TestCase):

    def test_filename(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        self.assertEqual(file_url.filename, 'text.txt')

    def test_filename_with_space(self):
        file_url = file_url_split.FileUrlSplit('/home/user/the text.txt')
        self.assertEqual(file_url.filename, 'the text.txt')

    def test_filename_without_extension(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text')
        self.assertEqual(file_url.filename, 'text')

    def test_hidden_filename(self):
        file_url = file_url_split.FileUrlSplit('/home/user/.the text.txt')
        self.assertEqual(file_url.filename, '.the text.txt')

    def test_hidden_filename_without_extension(self):
        file_url = file_url_split.FileUrlSplit('/home/user/.text')
        self.assertEqual(file_url.filename, '.text')


class TestFilenameSetter(unittest.TestCase):

    def test_new_filename(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        file_url.filename = 'foo.png'
        self.assertEqual(file_url.filename, 'foo.png')
        self.assertEqual(file_url.name, 'foo')
        self.assertEqual(file_url.url, '/home/user/foo.png')
        self.assertEqual(file_url.extension, '.png')

    def test_remove_filename(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        file_url.filename = ''
        self.assertEqual(file_url.filename, '')
        self.assertEqual(file_url.name, '')
        self.assertEqual(file_url.url, '/home/user/')
        self.assertEqual(file_url.extension, '')


class TestFilenameRaises(unittest.TestCase):

    def test_new_filename_raises(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        self.assertRaises(
            file_url_split.InvalidCharacterError,
            setattr, file_url, 'filename', '/foo.txt')

    def test_very_big_new_filename_raises(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        new_name = 'A' * 256
        self.assertRaises(
            file_url_split.FilenameTooLongError,
            setattr, file_url, 'filename', new_name)


if __name__ == '__main__':
    # No third-party testing coverage
    unittest.main()  # pragma: no cover
