"""Data models for PyClip2Playlist."""

from dataclasses import dataclass
from typing import List

@dataclass
class Song:
    """Represents a song with title and artist."""
    title: str
    artist: str

    def to_dict(self) -> dict:
        """Convert the song to a dictionary format.
        
        Returns:
            dict: Dictionary with TITLE and ARTIST keys.
        """
        return {
            'TITLE': self.title,
            'ARTIST': self.artist
        }

class SongCollection:
    """Manages a collection of songs."""
    
    def __init__(self):
        """Initialize an empty song collection."""
        self.songs: List[Song] = []
    
    def add_song(self, song: Song) -> None:
        """Add a song to the collection.
        
        Args:
            song: The Song object to add.
        """
        self.songs.append(song)
    
    def remove_song(self, index: int) -> None:
        """Remove a song at the specified index.
        
        Args:
            index: Index of the song to remove.
        """
        if 0 <= index < len(self.songs):
            self.songs.pop(index)
    
    def update_song(self, index: int, song: Song) -> None:
        """Update a song at the specified index.
        
        Args:
            index: Index of the song to update.
            song: New Song object.
        """
        if 0 <= index < len(self.songs):
            self.songs[index] = song
    
    def to_dict_list(self) -> List[dict]:
        """Convert all songs to a list of dictionaries.
        
        Returns:
            List of dictionaries with TITLE and ARTIST keys.
        """
        return [song.to_dict() for song in self.songs]
    
    def __len__(self) -> int:
        """Return the number of songs in the collection."""
        return len(self.songs)
