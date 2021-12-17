#!/usr/bin/python
# -*- encoding: utf-8 -*-
import unittest

from tinytag import TinyTag

mp3_file = TinyTag.get('testfiles/music/musicfox_dancing_street.mp3')
wav_file = TinyTag.get('testfiles/music/testFile.wav')
audio_book_file = TinyTag.get('testfiles/audiobooks/Paw Patrol/Track 1.wav')


class TestReadingMetaData(unittest.TestCase):

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

    def test_reading_image(self):
        image = audio_book_file.get_image()
        audio_book_file.disc_total
        audio_book_file.track_total
        # filesize sollte vllt nicht größer als 100mb sein also 100000000
        size = audio_book_file.filesize
        # audio_book_file.is_supported()
        duration = audio_book_file.duration
        audio_book_file.track
        print(image)

