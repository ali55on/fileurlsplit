#!/usr/bin/env python3
import sys
import unittest

import src.fileurlsplit as file_url_split

platform = sys.platform


class TestWindowsCharacterRaises(unittest.TestCase):

    def setUp(self) -> None:
        sys.platform = 'win32'

    def tearDown(self) -> None:
        sys.platform = platform

    def test_new_url_raises(self):
        file_url = file_url_split.FileUrlSplit('C:/windows/user/text.txt')
        self.assertRaises(
            file_url_split.InvalidCharacterError,
            setattr, file_url, 'url', 'C:/windows/user/Downloads/new|text.txt')
        self.assertRaises(
            file_url_split.InvalidCharacterError,
            setattr, file_url, 'url', 'C:/windows/user/Downloads*/text.txt')

    def test_new_name_raises(self):
        file_url = file_url_split.FileUrlSplit(r'c:\home\user\text.txt')
        self.assertRaises(
            file_url_split.InvalidCharacterError,
            setattr, file_url, 'name', 'new*text')

    def test_new_filename_raises(self):
        file_url = file_url_split.FileUrlSplit('C:/windows/home/user/text.txt')
        self.assertRaises(
            file_url_split.InvalidCharacterError,
            setattr, file_url, 'filename', 'new|name.text')

    def test_new_extension_raises(self):
        file_url = file_url_split.FileUrlSplit(r'c:\home\user\text.txt')
        self.assertRaises(
            file_url_split.InvalidCharacterError,
            setattr, file_url, 'name', '.>jpg')


class TestWindowsFilenameRaises(unittest.TestCase):

    def setUp(self) -> None:
        sys.platform = 'win32'

    def tearDown(self) -> None:
        sys.platform = platform

    def test_invalid_filename_raises(self):
        file_url = file_url_split.FileUrlSplit(r'c:\home\user\text.txt')
        self.assertRaises(
            file_url_split.InvalidFilenameError,
            setattr, file_url, 'filename', 'AUX')

    def test_invalid_path_raises(self):
        file_url = file_url_split.FileUrlSplit(r'c:\home\user\text.txt')
        self.assertRaises(
            file_url_split.InvalidFilenameError,
            setattr, file_url, 'path', 'c:\\windows\\AUX\\text.txt')


class TestMacCharacterRaises(unittest.TestCase):

    def setUp(self) -> None:
        sys.platform = 'darwin'

    def tearDown(self) -> None:
        sys.platform = platform

    def test_new_url_raises(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        self.assertRaises(
            file_url_split.InvalidCharacterError,
            setattr, file_url, 'name', 'new:text')


class TestBSDCharacterRaises(unittest.TestCase):

    def setUp(self) -> None:
        sys.platform = 'freebsd8'

    def tearDown(self) -> None:
        sys.platform = platform

    def test_new_url_raises(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        self.assertRaises(
            file_url_split.InvalidCharacterError,
            setattr, file_url, 'name', 'new:text')


class TestAnotherCharacterRaises(unittest.TestCase):

    def setUp(self) -> None:
        sys.platform = 'riscos'

    def tearDown(self) -> None:
        sys.platform = platform

    def test_new_url_raises(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        self.assertRaises(
            file_url_split.InvalidCharacterError,
            setattr, file_url, 'name', 'new>text')


if __name__ == '__main__':
    # No third-party testing coverage
    unittest.main()  # pragma: no cover
