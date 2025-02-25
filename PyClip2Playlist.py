#!/usr/bin/env python3
"""Starter script for PyClip2Playlist."""

from pyclip2playlist.gui import PyClip2PlaylistGUI

def main():
    """Start the PyClip2Playlist application."""
    app = PyClip2PlaylistGUI()
    app.run()

if __name__ == '__main__':
    main()
