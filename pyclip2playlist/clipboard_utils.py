"""Clipboard interaction utilities."""

import pyperclip

def load_clipboard() -> str:
    """Return the current content of the system clipboard.
    
    Returns:
        str: The current clipboard content.
    """
    return pyperclip.paste()
