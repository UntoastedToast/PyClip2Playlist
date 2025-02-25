"""Main entry point for running PyClip2Playlist."""

def main():
    """Main entry point for the application."""
    from pyclip2playlist.gui import PyClip2PlaylistGUI
    app = PyClip2PlaylistGUI()
    app.run()

if __name__ == '__main__':
    main()
