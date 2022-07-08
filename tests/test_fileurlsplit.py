#!/usr/bin/env python3
import unittest

import src.fileurlsplit as file_url_split


class TestUrl(unittest.TestCase):
    def setUp(self):
        pass

    def test_repr_obj(self):
        self.assertEqual(
            repr(file_url_split.FileUrlSplit('/home/user/text.txt')),
            "<FileUrlSplit '/home/user/text.txt'>")

    def test_raises(self):
        self.assertRaises(
            ValueError, file_url_split.FileUrlSplit, 'home/user/text.txt')


if __name__ == '__main__':
    # No third-party testing coverage
    unittest.main()  # pragma: no cover
