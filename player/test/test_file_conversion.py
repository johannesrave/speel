#!/usr/bin/python
# -*- encoding: utf-8 -*-
from unittest import TestCase
from pydub import AudioSegment


class FileConversionTest(TestCase):

    def test_wav_to_mp3(self):
        mp3_file = AudioSegment.from_wav("/testfiles/music/testFile.wav").export("/testfiles/output/testfile.mp3",
                                                                                 format="mp3")
