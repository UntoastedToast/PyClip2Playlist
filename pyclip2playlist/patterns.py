import re

patterns = [
    # Pattern 0: Numbered list with timestamp and title-artist.
    # Example:
    #   1. 0:03 - If You Want It - Niteflyte
    #   17. 1:00:08 - Each Time You Pray - Ned Doheny
    re.compile(
        r'^\s*'
        r'(?:\d+[\.\)]\s*)?'                         # Optional number with dot/parenthesis
        r'(?:(\d+:)?\d{1,2}:\d{2})\s*-?\s*'         # Time stamp (optional hour)
        r'(?P<track>.+?)\s*-\s*(?P<artist>.+?)'      # Title and artist separated by hyphen
        r'\s*$'
    ),

    # Pattern 1: Quoted title with time and artist in parentheses.
    # Example:
    #   1) 0:10 "Skate Dancer" (Doug Willis);
    #   3) 7:51 "Dance Your Blues Away (Edit-Bonus Track)" (Cosmic Boogie);
    #   10) 29:57 "Hail To the Teeth (Barrio Elect 12" ReEdit)" (District Of Columbia);
    re.compile(
        r'^\s*'
        r'(?:\d+[\.\)]\s+)?'                         # Optional numbering e.g. "1) " or "10. "
        r'(?P<time>\d{1,2}:\d{2}(?::\d{2})?)\s+'       # Time stamp e.g. "0:10" or "7:51"
        r'"(?P<track>.*?)(?="\s+\()"\s+'              # Non-greedy capture for track until the closing quote that is immediately followed by whitespace and an opening parenthesis
        r'\((?P<artist>[^)]+)\)'                      # Artist captured inside parentheses
        r'[;\.]?\s*$'                                # Optional semicolon or period at the end
    ),

    # Pattern 2: Simple format with time, title, and artist separated by a hyphen.
    # Example:
    #   00:16 Summer Breeze - Piper
    re.compile(
        r'^\s*'
        r'(?P<time>\d{1,2}:\d{2}(?::\d{2})?)\s+'       # Time stamp
        r'(?P<track>.+?)\s*-\s*(?P<artist>.+?)'         # Title and artist separated by hyphen
        r'[;\.]?\s*$'
    ),

    # Pattern 3: Format without a time stamp, simply "Title - Artist".
    # Example:
    #   Nana kinomi - Omaesan
    re.compile(
        r'^\s*'
        r'(?P<track>.+?)\s*-\s*(?P<artist>.+?)\s*$'
    ),

    # Pattern 4: Reversed order "Artist: Title"
    # Example:
    #   Michael Boothman: Waiting for Your Love
    re.compile(
        r'^\s*'
        r'(?P<artist>.+?)\s*:\s*(?P<track>.+?)\s*$'
    ),

    # Pattern 5: Format with "by" as the separator (case-insensitive).
    # Example:
    #   Summer Breeze by Piper
    re.compile(
        r'^\s*'
        r'(?P<track>.+?)\s+by\s+(?P<artist>.+?)\s*$',
        re.IGNORECASE
    ),

    # Pattern 6: Format using Unicode dashes (en dash or em dash) as the separator.
    # Example:
    #   Track Title – Artist Name   OR   Track Title — Artist Name
    re.compile(
        r'^\s*'
        r'(?P<track>.+?)\s*[–—]\s*(?P<artist>.+?)'
        r'(?:\s+\d{1,2}:\d{2}(?::\d{2})?)?\s*$'
    ),

    # Pattern 7: Pipe-separated format.
    # Example:
    #   Track Title | Artist Name
    re.compile(
        r'^\s*'
        r'(?P<track>.+?)\s*\|\s*(?P<artist>.+?)\s*$'
    ),

    # Pattern 8: Quoted title (using curly or straight quotes) with a Unicode dash separator.
    # Example:
    #   3) 7:51 “Dance Your Blues Away (Edit-Bonus Track)” – Cosmic Boogie
    re.compile(
        r'^\s*'
        r'(?:\d+[\.\)]\s+)?'
        r'(?P<time>\d{1,2}:\d{2}(?::\d{2})?)\s+'
        r'[“"](?P<track>.*?)[”"]\s*[–—]\s*'
        r'(?P<artist>.+?)'
        r'[;\.]?\s*$'
    ),
]
