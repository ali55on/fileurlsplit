#!/usr/bin/env python3
import logging
import sys
import unittest

import src.fileurlsplit as file_url_split


class TestMessageErrors(unittest.TestCase):

    def setUp(self) -> None:
        self.platform = sys.platform
        self.text_255_chars = 'text_' * 50 + '.html'

    def tearDown(self) -> None:
        sys.platform = self.platform

    def test_file_too_long_error_message(self):
        file_url = file_url_split.FileUrlSplit()
        try:
            file_url.url = '/home/user/c_' + self.text_255_chars
        except file_url_split.FilenameTooLongError as er:
            logging.info(er.message)

    def test_absolute_path_error_message(self):
        file_url = file_url_split.FileUrlSplit()
        try:
            file_url.path = 'home/user/'
        except file_url_split.AbsolutePathError as er:
            logging.info(er.message)

    def test_invalid_char_error_message(self):
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        try:
            file_url.name = 'text/works'
        except file_url_split.InvalidCharacterError as er:
            logging.info(er.message)
            logging.info(er.invalid_character_found)
            logging.info(er.all_invalid_characters_list)

    def test_invalid_filename_error_message(self):
        sys.platform = 'win32'
        file_url = file_url_split.FileUrlSplit('/home/user/text.txt')
        try:
            file_url.filename = 'AUX'
        except file_url_split.InvalidFilenameError as er:
            logging.info(er.message)
            logging.info(er.all_invalid_filename_list)
        sys.platform = self.platform
