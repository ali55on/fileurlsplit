#!/usr/bin/env python3
import unittest

import src.fileurlsplit as file_url_split


class TestFilename(unittest.TestCase):
    def setUp(self):
        pass

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


if __name__ == '__main__':
    unittest.main()
