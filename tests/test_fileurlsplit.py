#!/usr/bin/env python3
import unittest

import src.fileurlsplit as file_url_split


class TestFileUrlSplit(unittest.TestCase):

    def test_repr_obj(self):
        self.assertEqual(
            repr(file_url_split.FileUrlSplit('/home/user/text.txt')),
            'FileUrlSplit("/home/user/text.txt")')

    def test_only_path_without_file(self):
        file_url = file_url_split.FileUrlSplit('/home/user/')
        self.assertEqual(file_url.url, '/home/user/')
        self.assertEqual(file_url.path, '/home/user/')
        self.assertEqual(file_url.filename, '')
        self.assertEqual(file_url.name, '')
        self.assertEqual(file_url.extension, '')


class TestFileUrlSplitRaises(unittest.TestCase):

    def test_non_absolute_path_raises(self):
        self.assertRaises(
            file_url_split.AbsolutePathError,
            file_url_split.FileUrlSplit, 'home/user/text.txt')

    def test_non_absolute_path_with_file_prefix_raises(self):
        self.assertRaises(
            file_url_split.AbsolutePathError,
            file_url_split.FileUrlSplit, 'file:home/user/text.txt')


if __name__ == '__main__':
    # No third-party testing coverage
    unittest.main()  # pragma: no cover
