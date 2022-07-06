#!/usr/bin/env python3
# python3 -m unittest discover
# python3 -m unittest
# python3 -m unittest tests.test_extensions
import unittest

import src.fileurlsplit as file_url_split


class TestExtensions(unittest.TestCase):
    def setUp(self):
        pass

    def test_extension(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        self.assertEqual(file_url.extension, '.txt')

    def test_extension_on_hidden_file(self):
        file_url = file_url_split.FileUrlSplit('/home/user/.text.txt')
        self.assertEqual(file_url.extension, '.txt')

    def test_no_extension(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text')
        self.assertEqual(file_url.extension, '')

    def test_no_extension_on_hidden_file(self):
        file_url = file_url_split.FileUrlSplit('/home/user/.text')
        self.assertEqual(file_url.extension, '')

    def test_no_extension_if_it_ends_with_a_dot(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.')
        self.assertEqual(file_url.extension, '')

    def test_no_extension_on_hidden_file_if_it_ends_with_a_dot(self):
        file_url = file_url_split.FileUrlSplit('/home/user/.text.')
        self.assertEqual(file_url.extension, '')

    def test_internal_extension(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.tar.gz')
        self.assertEqual(file_url.extension, '.tar.gz')

    def test_complex_internal_extension(self):
        file_url = file_url_split.FileUrlSplit('/home/user/todo.text.tar.gz')
        self.assertEqual(file_url.extension, '.tar.gz')

    def test_complex_extension(self):
        file_url = file_url_split.FileUrlSplit('/home/user/todo.text.ta.gz')
        self.assertEqual(file_url.extension, '.gz')


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
