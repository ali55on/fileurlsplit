#!/usr/bin/env python3
import unittest

import src.fileurlsplit as file_url_split


class TestUrl(unittest.TestCase):
    def setUp(self):
        pass

    def test_url(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        self.assertEqual(file_url.url, '/home/user/text.txt')

    def test_url_with_file_prefix(self):
        file_url = file_url_split.FileUrlSplit('file:///home/user/text.txt')
        self.assertEqual(file_url.url, '/home/user/text.txt')

    def test_url_with_dos_prefix(self):
        file_url = file_url_split.FileUrlSplit('c:/home/user/text.txt')
        self.assertEqual(file_url.url, '/home/user/text.txt')

    def test_dos_url_with_scape(self):
        file_url = file_url_split.FileUrlSplit('c:\\windows\\user\\text.txt')
        self.assertEqual(file_url.url, '/windows/user/text.txt')

    def test_dos_url_without_scape_using_raw_string(self):
        file_url = file_url_split.FileUrlSplit(r'c:\windows\user\text.txt')
        self.assertEqual(file_url.url, '/windows/user/text.txt')


if __name__ == '__main__':
    unittest.main()
