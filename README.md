# PyClip2Playlist 📋➡️🎵

PyClip2Playlist is a Python-based application that converts clipboard content into a formatted playlist. It extracts data from your clipboard and applies configurable patterns to generate playlists, allowing seamless integration with media applications and workflows.

## Features ✨

- **Clipboard Integration:** 📎 Captures text content from your clipboard.
- **Pattern Matching:** 🔍 Uses customizable patterns defined in `patterns.py` to parse and transform clipboard data into playlist entries.
- **Playlist Creation:** 🎵 Generates a playlist based on recognized patterns.
- **Extensibility:** 🔧 Additional patterns can be added via the `patterns.py` module to support more formats or data.

## Installation 🚀

1. **Install Python:** 🐍 Ensure Python (version 3.6 or higher) is installed on your system. [Python Download](https://www.python.org/downloads/)

2. **Clone Repository:**

   ```bash
   git clone https://github.com/UntoastedToast/PyClip2Playlist.git
   cd PyClip2Playlist
   ```

3. **Install Dependencies:**  
   Install the required packages using pip:
   
   ```bash
   pip install -r requirements.txt
   ```

## Usage 🎮

Run the script to read the clipboard and create a playlist:

```bash
python PyClip2Playlist.py
```

The process reads the current clipboard content, searches for matching patterns, and outputs the result as a playlist.

## Adding Patterns ⚙️

The [`patterns.py`](patterns.py) module contains the regex patterns that the program uses to detect relevant data. To add new patterns:

1. Open the `patterns.py` file.
2. Add a new regex pattern as a new entry to the patterns list.
3. Ensure the pattern is tested and properly formatted to match the clipboard content.

Example for a new pattern:

```python
# Example Python code in patterns.py
my_new_pattern = r"your-regex-pattern-here"
patterns.append(my_new_pattern)
```

## License 📄

This project is licensed under the [MIT License](LICENSE).

## Support 💬

If you have any questions or issues, please create an issue in the GitHub repository.
