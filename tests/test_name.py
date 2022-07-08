#!/usr/bin/env python3
import unittest

import src.fileurlsplit as file_url_split


class TestName(unittest.TestCase):
    def setUp(self):
        pass

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

    def test_new_name(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        file_url.name = 'foo'
        self.assertEqual(file_url.name, 'foo')
        self.assertEqual(file_url.url, '/home/user/foo.txt')
        self.assertEqual(file_url.filename, 'foo.txt')
        self.assertEqual(file_url.path, '/home/user/')
        self.assertEqual(file_url.extension, '.txt')

    def test_new_name_raises(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        self.assertRaises(
            ValueError, setattr, file_url, 'name', '/foo')


if __name__ == '__main__':
    # No third-party testing coverage
    unittest.main()  # pragma: no cover
