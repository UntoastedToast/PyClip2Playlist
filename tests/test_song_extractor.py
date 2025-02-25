"""Test suite for song extraction functionality."""

import unittest
from pyclip2playlist.song_extractor import extract_songs, fallback_extraction
from pyclip2playlist.models import Song

class TestSongExtractor(unittest.TestCase):
    """Test cases for song extraction functionality."""

    def test_pattern1_quoted_title_with_time(self):
        """Test quoted title with time and artist in parentheses."""
        text = '1) 0:10 "Skate Dancer" (Doug Willis);'
        result = extract_songs(text)
        self.assertEqual(result[0], {'TITLE': 'Skate Dancer', 'ARTIST': 'Doug Willis'})

    def test_pattern2_time_title_artist(self):
        """Test simple format with time, title, and artist separated by hyphen."""
        text = '00:16 Summer Breeze - Piper'
        result = extract_songs(text)
        self.assertEqual(result[0], {'TITLE': 'Summer Breeze', 'ARTIST': 'Piper'})

    def test_pattern3_simple_title_artist(self):
        """Test format without time stamp, simply Title - Artist."""
        text = 'Nana kinomi - Omaesan'
        result = extract_songs(text)
        self.assertEqual(result[0], {'TITLE': 'Nana kinomi', 'ARTIST': 'Omaesan'})

    def test_pattern4_artist_title(self):
        """Test reversed order Artist: Title."""
        text = 'Michael Boothman: Waiting for Your Love'
        result = extract_songs(text)
        self.assertEqual(result[0], {'TITLE': 'Waiting for Your Love', 'ARTIST': 'Michael Boothman'})

    def test_pattern5_title_by_artist(self):
        """Test format with 'by' as separator."""
        text = 'Summer Breeze by Piper'
        result = extract_songs(text)
        self.assertEqual(result[0], {'TITLE': 'Summer Breeze', 'ARTIST': 'Piper'})

    def test_fallback_extraction_hyphen(self):
        """Test fallback extraction with hyphen separator."""
        title, artist = fallback_extraction('Title - Artist')
        self.assertEqual(title, 'Title')
        self.assertEqual(artist, 'Artist')

    def test_fallback_extraction_colon(self):
        """Test fallback extraction with colon separator."""
        title, artist = fallback_extraction('Artist: Title')
        self.assertEqual(title, 'Title')
        self.assertEqual(artist, 'Artist')

    def test_fallback_extraction_by(self):
        """Test fallback extraction with 'by' separator."""
        title, artist = fallback_extraction('Track by Artist')
        self.assertEqual(title, 'Track')
        self.assertEqual(artist, 'Artist')

    def test_extract_multiple_songs(self):
        """Test extracting multiple songs from text."""
        text = '''1) 0:10 "Skate Dancer" (Doug Willis);
                 00:16 Summer Breeze - Piper
                 Nana kinomi - Omaesan'''
        result = extract_songs(text)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], {'TITLE': 'Skate Dancer', 'ARTIST': 'Doug Willis'})
        self.assertEqual(result[1], {'TITLE': 'Summer Breeze', 'ARTIST': 'Piper'})
        self.assertEqual(result[2], {'TITLE': 'Nana kinomi', 'ARTIST': 'Omaesan'})

    def test_malformed_input(self):
        """Test handling of malformed input."""
        text = 'This is not a song'
        result = extract_songs(text)
        self.assertEqual(result[0], {'TITLE': 'This is not a song', 'ARTIST': 'Unknown'})

    def test_empty_input(self):
        """Test handling of empty input."""
        text = ''
        result = extract_songs(text)
        self.assertEqual(result, [])

    def test_whitespace_handling(self):
        """Test proper handling of whitespace."""
        text = '  Artist  :  Title  '
        result = extract_songs(text)
        self.assertEqual(result[0], {'TITLE': 'Title', 'ARTIST': 'Artist'})

if __name__ == '__main__':
    unittest.main()
