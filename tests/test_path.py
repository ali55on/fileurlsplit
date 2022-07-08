#!/usr/bin/env python3
import unittest

import src.fileurlsplit as file_url_split


class TestPath(unittest.TestCase):
    def setUp(self):
        pass

    def test_path(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        self.assertEqual(file_url.path, '/home/user/')

    def test_path_in_filename_without_extension(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text')
        self.assertEqual(file_url.path, '/home/user/')

    def test_only_path(self):
        file_url = file_url_split.FileUrlSplit('/home/user/')
        self.assertEqual(file_url.path, '/home/user/')

    def test_new_path(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        file_url.path = '/home/user/Downloads'
        self.assertEqual(file_url.path, '/home/user/Downloads/')

    def test_new_path_raises(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        # Works
        self.assertRaises(
            ValueError, setattr, file_url, 'path', 'home/user/Downloads')
        # Also works
        with self.assertRaises(ValueError):
            file_url.path = 'home/user/Downloads'


if __name__ == '__main__':
    # No third-party testing coverage
    unittest.main()  # pragma: no cover
