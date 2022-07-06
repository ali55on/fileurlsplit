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


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
