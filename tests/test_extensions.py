#!/usr/bin/env python3
# python3 -m unittest discover
# python3 -m unittest
# python3 -m unittest tests.test_extensions
import unittest

import src.fileurlsplit as file_url_split


class TestExtensions(unittest.TestCase):

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

    def test_new_extension(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        file_url.extension = '.pdf'
        self.assertEqual(file_url.extension, '.pdf')
        self.assertEqual(file_url.url, '/home/user/text.pdf')
        self.assertEqual(file_url.filename, 'text.pdf')

    def test_new_extension_without_a_dot(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        file_url.extension = 'pdf'
        self.assertEqual(file_url.extension, '.pdf')
        self.assertEqual(file_url.url, '/home/user/text.pdf')
        self.assertEqual(file_url.filename, 'text.pdf')


class TestExtensionsRaises(unittest.TestCase):

    def test_new_extension_raises(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        self.assertRaises(
            file_url_split.InvalidCharacterError,
            setattr, file_url, 'extension', '/pdf')

    def test_very_big_new_name_with_extension_raises(self):
        file_url = file_url_split.FileUrlSplit('/home/user/x.txt')
        new_extension = 'x' * 255
        self.assertRaises(
            file_url_split.FilenameTooLongError,
            setattr, file_url, 'extension', new_extension)
        self.assertRaises(
            file_url_split.FilenameTooLongError,
            setattr, file_url, 'extension', '.' + new_extension)

    def test_very_big_new_name_without_extension_raises(self):
        file_url = file_url_split.FileUrlSplit('/home/user/x')
        new_extension = 'x' * 255
        self.assertRaises(
            file_url_split.FilenameTooLongError,
            setattr, file_url, 'extension', new_extension)
        self.assertRaises(
            file_url_split.FilenameTooLongError,
            setattr, file_url, 'extension', '.' + new_extension)


if __name__ == '__main__':
    # No third-party testing coverage
    unittest.main()  # pragma: no cover
