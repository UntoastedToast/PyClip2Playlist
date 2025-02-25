"""Clipboard interaction utilities."""

import pyperclip
import logging  # Added logging

def load_clipboard() -> str:
    """Return the current content of the system clipboard.
    
    Returns:
        str: The current clipboard content.
    """
    try:
        content = pyperclip.paste()
        # Ensure proper UTF-8 encoding
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        # Normalize line endings
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        # Remove any BOM if present
        content = content.replace('\ufeff', '')
        return content
    except Exception as e:
        logging.error("Error reading clipboard: %s", e)
        return ""
