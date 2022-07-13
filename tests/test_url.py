#!/usr/bin/env python3
import unittest

import src.fileurlsplit as file_url_split


class TestUrlProperty(unittest.TestCase):

    def test_url(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        self.assertEqual(file_url.url, '/home/user/text.txt')

    def test_url_only_path_without_file(self):
        file_url = file_url_split.FileUrlSplit('/home/user/')
        self.assertEqual(file_url.url, '/home/user/')
        self.assertEqual(file_url.path, '/home/user/')
        self.assertEqual(file_url.filename, '')
        self.assertEqual(file_url.name, '')
        self.assertEqual(file_url.extension, '')

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

    def test_none_str_url(self):
        file_url = file_url_split.FileUrlSplit('')
        self.assertEqual(file_url.url, '/')
        self.assertEqual(file_url.path, '/')
        self.assertEqual(file_url.filename, '')
        self.assertEqual(file_url.name, '')
        self.assertEqual(file_url.extension, '')

    def test_none_url(self):
        file_url = file_url_split.FileUrlSplit(None)
        self.assertEqual(file_url.url, '/')
        self.assertEqual(file_url.path, '/')
        self.assertEqual(file_url.filename, '')
        self.assertEqual(file_url.name, '')
        self.assertEqual(file_url.extension, '')

    def test_empt_obj(self):
        file_url = file_url_split.FileUrlSplit()
        self.assertEqual(file_url.url, '/')
        self.assertEqual(file_url.path, '/')
        self.assertEqual(file_url.filename, '')
        self.assertEqual(file_url.name, '')
        self.assertEqual(file_url.extension, '')

    def test_min_path_url(self):
        file_url = file_url_split.FileUrlSplit('/')
        self.assertEqual(file_url.url, '/')
        self.assertEqual(file_url.path, '/')
        self.assertEqual(file_url.filename, '')
        self.assertEqual(file_url.name, '')
        self.assertEqual(file_url.extension, '')

        file_url = file_url_split.FileUrlSplit('/x/')
        self.assertEqual(file_url.url, '/x/')
        self.assertEqual(file_url.path, '/x/')
        self.assertEqual(file_url.filename, '')
        self.assertEqual(file_url.name, '')
        self.assertEqual(file_url.extension, '')

    def test_min_file_url(self):
        file_url = file_url_split.FileUrlSplit('/x')
        self.assertEqual(file_url.url, '/x')
        self.assertEqual(file_url.path, '/')
        self.assertEqual(file_url.filename, 'x')
        self.assertEqual(file_url.name, 'x')
        self.assertEqual(file_url.extension, '')

        file_url = file_url_split.FileUrlSplit('/tmp')
        self.assertEqual(file_url.url, '/tmp')
        self.assertEqual(file_url.path, '/')
        self.assertEqual(file_url.filename, 'tmp')
        self.assertEqual(file_url.name, 'tmp')
        self.assertEqual(file_url.extension, '')


class TestUrlSetter(unittest.TestCase):

    def test_new_pure_url(self):
        file_url = file_url_split.FileUrlSplit('file:///home/user/text.txt')
        file_url.url = '/home/user/Downloads/image.png'
        self.assertEqual(file_url.url, '/home/user/Downloads/image.png')
        self.assertEqual(file_url.path, '/home/user/Downloads/')
        self.assertEqual(file_url.name, 'image')
        self.assertEqual(file_url.filename, 'image.png')
        self.assertEqual(file_url.extension, '.png')

    def test_new_prefix_url(self):
        file_url = file_url_split.FileUrlSplit('file:///home/user/text.txt')
        file_url.url = 'file:/home/user/Downloads/image.png'
        self.assertEqual(file_url.url, '/home/user/Downloads/image.png')
        self.assertEqual(file_url.path, '/home/user/Downloads/')
        self.assertEqual(file_url.name, 'image')
        self.assertEqual(file_url.filename, 'image.png')
        self.assertEqual(file_url.extension, '.png')

        file_url.url = 'file:///home/user/Documents/image.png'
        self.assertEqual(file_url.url, '/home/user/Documents/image.png')

        file_url.url = 'c:/home/user/Desktop/image.png'
        self.assertEqual(file_url.url, '/home/user/Desktop/image.png')

    def test_empt_obj_and_set_url(self):
        file_url = file_url_split.FileUrlSplit()
        self.assertEqual(file_url.url, '/')
        self.assertEqual(file_url.path, '/')
        self.assertEqual(file_url.filename, '')
        self.assertEqual(file_url.name, '')
        self.assertEqual(file_url.extension, '')

        file_url.url = '/my/dummy/URL.test'
        self.assertEqual(file_url.url, '/my/dummy/URL.test')
        self.assertEqual(file_url.path, '/my/dummy/')
        self.assertEqual(file_url.filename, 'URL.test')
        self.assertEqual(file_url.name, 'URL')
        self.assertEqual(file_url.extension, '.test')

    def test_new_url_like_a_path(self):
        file_url = file_url_split.FileUrlSplit('file:///home/user/text.txt')
        file_url.url = '/home/user/'
        self.assertEqual(file_url.url, '/home/user/')
        self.assertEqual(file_url.path, '/home/user/')
        self.assertEqual(file_url.filename, '')
        self.assertEqual(file_url.name, '')
        self.assertEqual(file_url.extension, '')


class TestUrlRaises(unittest.TestCase):

    def test_new_relative_url_raises(self):
        file_url = file_url_split.FileUrlSplit('file:///home/user/text.txt')
        self.assertRaises(
            file_url_split.AbsolutePathError,
            setattr, file_url, 'url', 'user/Downloads/text.txt')


if __name__ == '__main__':
    # No third-party testing coverage
    unittest.main()  # pragma: no cover
