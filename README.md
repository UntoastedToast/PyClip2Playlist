# PyClip2Playlist

Extract song information from clipboard text and create playlists. This application allows you to easily convert text containing song information (in various formats) into a structured CSV playlist.

## Features

- Extract song titles and artists from clipboard text in multiple formats
- Support for various text formats including:
  - Time-stamped tracks with quoted titles and artists in parentheses
  - Simple "Title - Artist" format
  - "Artist: Title" format
  - "Title by Artist" format
  - And more...
- GUI interface for easy interaction
- Live clipboard monitoring
- CSV export functionality
- Edit capabilities for extracted songs
- Right-click context menu for song deletion

## Installation

You can install PyClip2Playlist directly from PyPI:
```bash
pip install pyclip2playlist
```

Or install from source for development:
```bash
# Clone the repository
git clone https://github.com/UntoastedToast/PyClip2Playlist.git
cd PyClip2Playlist

# Create and activate virtual environment (recommended)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install in development mode
pip install -e .
```

## Usage

There are several ways to run the application:

### Direct Run (without installation)
After cloning the repository, you can run the application directly:
```bash
# Windows
python pyclip2playlist.py

# Linux/Mac
python3 pyclip2playlist.py
# or make it executable and run:
chmod +x pyclip2playlist.py
./pyclip2playlist.py
```

### After Installation
After installing the package, you can run it in one of these ways:

1. Using the command line tool:
```bash
pyclip2playlist
```

2. As a Python module:
```bash
python -m pyclip2playlist
```

## Development

For development, after cloning the repository:

1. Set up your development environment as described in the installation section.

2. To publish a new version to PyPI, use the provided scripts:

   On Windows:
   ```bash
   cd scripts
   .\publish.bat
   ```

   On Linux/Mac:
   ```bash
   cd scripts
   chmod +x publish.sh
   ./publish.sh
   ```

   Note: You'll need a PyPI account and appropriate permissions to publish.

### How to Use

1. Copy text containing song information to your clipboard
2. Press "Refresh Clipboard" in the application to load the clipboard content
3. Click "Extract Songs" to parse the text and extract song information
4. Edit any entries if needed by double-clicking on them
5. Save the extracted songs as a CSV file using the "Save CSV" button or File menu

### Supported Text Formats

The application supports various text formats, including but not limited to:

```
1) 0:10 "Skate Dancer" (Doug Willis);
00:16 Summer Breeze - Piper
Nana kinomi - Omaesan
Michael Boothman: Waiting for Your Love
Summer Breeze by Piper
Track Title | Artist Name
```

## Requirements

- Python 3.8 or higher
- pyperclip>=1.8.2

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
