#!/usr/bin/python
# -*- encoding: utf-8 -*-
import unittest

import audiotools
from audiotools import musicbrainz
from tinytag import TinyTag

track_with_metadata = 'testfiles/trackWithMetaData.wav'
mp3_file_path = 'testfiles/music/musicfox_dancing_street.mp3'
mp3_file = TinyTag.get(mp3_file_path)
wav_file_path = 'testfiles/music/testFile.wav'
wav_file = TinyTag.get(wav_file_path)
audio_book_file_path = 'testfiles/audiobooks/Paw Patrol/Track 1.wav'
audio_book_file = TinyTag.get(audio_book_file_path)


class TestReadingMetaData(unittest.TestCase):
    # read metadata for single songs with Tinytag and if title is empty just take filename as title (for albums use
    # musicbrainz)
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

    def test_read_non_existing_title(self):
        actual_title = wav_file.title
        expected_title = None
        self.assertEqual(expected_title, actual_title)

    # read metadata for albums with musicbrainz
    def test_reading_metadata_from_musicbrainz(self):
        album_tracks = list(audiotools.open_directory('testfiles/audiobooks/Connie'))
        music_brainz_disc_id = musicbrainz.DiscID.from_tracks(album_tracks)
        metadata_generator = audiotools.musicbrainz.perform_lookup(music_brainz_disc_id, 'musicbrainz.org', 80)
        metadata_of_all_tracks = []
        for all_album_metadata in metadata_generator:
            if all_album_metadata:
                print(all_album_metadata)
                for track_metadata in all_album_metadata:
                    print(track_metadata)
                    metadata_of_all_tracks.append(track_metadata)

        self.assertEqual('Titelsong "Meine Freundin Conni"', metadata_of_all_tracks[0].track_name)
        self.assertEqual('Liane Schneider', metadata_of_all_tracks[0].artist_name)
        self.assertEqual(1, metadata_of_all_tracks[0].track_number, )
        self.assertEqual(9, metadata_of_all_tracks[0].track_total, )
        self.assertEqual(
            'Meine Freundin Conni, Volume 4: Conni hat Geburtstag / Conni backt Pizza / Conni geht in den Zoo / Conni geht verloren',
            metadata_of_all_tracks[0].album_name, )

        self.assertEqual('Conni backt Pizza (Teil 2)', metadata_of_all_tracks[4].track_name)

    def test_no_musicbrainz_metadata_exist_read_with_tinytag(self):
        album_tracks = list(audiotools.open_directory('testfiles/audiobooks/Connie'))
        music_brainz_disc_id = musicbrainz.DiscID.from_tracks(album_tracks)
        metadata_generator = audiotools.musicbrainz.perform_lookup(music_brainz_disc_id, 'musicbrainz.org', 80)
        metadata_of_all_tracks = []
