"""Song extraction functionality."""

from typing import List, Tuple, Dict, Optional
from .models import Song
from .patterns import patterns
import logging

def fallback_extraction(line: str) -> Tuple[Optional[str], Optional[str]]:
    """Extract title and artist using simple heuristics if regex patterns don't match.
    
    Args:
        line: Input line to extract from.
        
    Returns:
        Tuple of (title, artist) if extraction successful, (None, None) otherwise.
    """
    if '-' in line:
        parts = line.split('-', 1)
        title = parts[0].strip(" :;-")
        artist = parts[1].strip(" :;-")
        if title and artist:
            return title, artist

    if ':' in line:
        parts = line.split(':', 1)
        artist = parts[0].strip(" :;-")
        title = parts[1].strip(" :;-")
        if title and artist:
            return title, artist

    if ' by ' in line.lower():
        index = line.lower().find(' by ')
        title = line[:index].strip(" :;-")
        artist = line[index + 4:].trip(" :;-")
        if title and artist:
            return title, artist

    return None, None

def clean_text(text: str) -> str:
    """Clean and normalize the input text.
    
    Args:
        text: Input text to clean.
        
    Returns:
        str: Cleaned text.
    """
    # Remove "TITLEARTIST" header if present
    text = text.replace("TITLEARTIST", "")
    
    # Clean and normalize text
    text = text.replace('\u200b', '')  # Remove zero-width spaces
    text = text.replace('\ufeff', '')  # Remove BOM
    
    return text

def extract_songs(text: str) -> List[Dict[str, str]]:
    """Extract songs (title and artist) from text.
    
    The function tries regex patterns first; if none match, falls back to heuristic extraction.
    If all methods fail, uses the entire line as the title with "Unknown" artist.
    
    Args:
        text: Input text containing song information.
        
    Returns:
        List of dictionaries, each containing 'TITLE' and 'ARTIST' keys.
    """
    extracted = []
    
    # Clean the input text first
    text = clean_text(text)
    
    for line in text.splitlines():
        original_line = line
        line = line.strip()
        if not line:
            continue

        matched = False
        
        # Try regex patterns first
        for pattern in patterns:
            match = pattern.match(line)
            if match:
                title = match.group('track').strip()
                artist = match.group('artist').strip()
                song = Song(title=title, artist=artist)
                extracted.append(song.to_dict())
                matched = True
                break

        # Try fallback extraction if no pattern matched
        if not matched:
            title, artist = fallback_extraction(line)
            if title and artist:
                song = Song(title=title, artist=artist)
                extracted.append(song.to_dict())
                matched = True

        # Use entire line as title if all extraction methods failed
        if not matched:
            song = Song(title=line, artist="Unknown")
            extracted.append(song.to_dict())
            logging.warning("Fallback: Using entire line as title: %s", original_line)

    return extracted
