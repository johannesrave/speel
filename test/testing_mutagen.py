#!/usr/bin/python
# -*- encoding: utf-8 -*-
import unittest

from tinytag import TinyTag

path_to_mp3 = 'musicfox_dancing_street.mp3'
path_to_wav = 'testFile.wav'
mp3_file = TinyTag.get(path_to_mp3)
wav_file = TinyTag.get(path_to_wav)


class TestingMutagen(unittest.TestCase):

    def test_reading_length(self):
        actual_length_in_seconds = mp3_file.duration
        expected_length_in_seconds = 74.05714285714286
        self.assertEqual(expected_length_in_seconds, actual_length_in_seconds)

    def test_reading_title_from_mp3(self):
        actual_title = mp3_file.title
        expected_title = 'Dancing Street'
        self.assertEqual(expected_title, actual_title)

    def test_reading_artist(self):
        actual_artist = mp3_file.artist
        expected_artist = 'musicfox'
        self.assertEqual(expected_artist, actual_artist)

    def test_reading_length_of_wav(self):
        actual_length = wav_file.duration
        expected_length = 3.108730158730159
        self.assertEqual(expected_length, actual_length)
