#!/usr/bin/python
# -*- encoding: utf-8 -*-
import tempfile
from unittest import TestCase
import audiotools


class FileConversionTest(TestCase):

    def test_wav_to_mp3(self):
        mp3_file = audiotools.open("testfiles/music/testFile.wav").convert("testfiles/output/testFile.mp3", audiotools.MP3Audio)
        self.assertIsNotNone(mp3_file)

    def test_tempfile(self):
        tmp_file = tempfile.TemporaryFile()
        print(tmp_file)
