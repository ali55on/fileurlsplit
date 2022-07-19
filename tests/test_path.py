#!/usr/bin/env python3
import unittest

import src.fileurlsplit as file_url_split


class TestPathProperty(unittest.TestCase):

    def test_path(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        self.assertEqual(file_url.path, '/home/user/')

    def test_path_in_filename_without_extension(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text')
        self.assertEqual(file_url.path, '/home/user/')

    def test_only_path(self):
        file_url = file_url_split.FileUrlSplit('/home/user/')
        self.assertEqual(file_url.path, '/home/user/')


class TestPathSetter(unittest.TestCase):

    def test_new_pure_path(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        file_url.path = '/home/user/Downloads'
        self.assertEqual(file_url.path, '/home/user/Downloads/')
        self.assertEqual(file_url.url, '/home/user/Downloads/text.txt')

    def test_new_prefix_path(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        file_url.path = 'file:///home/user/Downloads'
        self.assertEqual(file_url.path, '/home/user/Downloads/')
        self.assertEqual(file_url.url, '/home/user/Downloads/text.txt')

        file_url.path = 'file:/home/user/Documents/'
        self.assertEqual(file_url.path, '/home/user/Documents/')
        self.assertEqual(file_url.url, '/home/user/Documents/text.txt')

        file_url.path = 'c:/home/user/Desktop'
        self.assertEqual(file_url.path, '/home/user/Desktop/')
        self.assertEqual(file_url.url, '/home/user/Desktop/text.txt')

    def test_remove_path(self):
        file_url = file_url_split.FileUrlSplit('file:///home/user/text.txt')
        file_url.path = ''
        self.assertEqual(file_url.url, '/text.txt')
        self.assertEqual(file_url.path, '/')
        self.assertEqual(file_url.filename, 'text.txt')
        self.assertEqual(file_url.name, 'text')
        self.assertEqual(file_url.extension, '.txt')

        file_url = file_url_split.FileUrlSplit('file:///home/user/text')
        file_url.path = ''
        self.assertEqual(file_url.url, '/text')
        self.assertEqual(file_url.path, '/')
        self.assertEqual(file_url.filename, 'text')
        self.assertEqual(file_url.name, 'text')
        self.assertEqual(file_url.extension, '')

        file_url = file_url_split.FileUrlSplit('file:///home/user/')
        file_url.path = ''
        self.assertEqual(file_url.url, '/')
        self.assertEqual(file_url.path, '/')
        self.assertEqual(file_url.filename, '')
        self.assertEqual(file_url.name, '')
        self.assertEqual(file_url.extension, '')


class TestPathRaises(unittest.TestCase):

    def test_absolute_path_raises(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        self.assertRaises(
            file_url_split.AbsolutePathError,
            setattr, file_url, 'path', 'home/user/Downloads')
        # Also works
        with self.assertRaises(file_url_split.AbsolutePathError):
            file_url.path = 'home/user/Downloads'

    def test_filename_too_long_raises(self):
        file_url = file_url_split.FileUrlSplit('file:///home/user/text.txt')
        text_255_chars = 'text_' * 50 + '.html'
        self.assertRaises(
            file_url_split.FilenameTooLongError,
            setattr, file_url, 'path', '/home/user/' + text_255_chars + '+/')


if __name__ == '__main__':
    # No third-party testing coverage
    unittest.main()  # pragma: no cover
