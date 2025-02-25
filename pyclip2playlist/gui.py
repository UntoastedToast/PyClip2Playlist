"""Graphical User Interface for PyClip2Playlist."""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import csv
import logging
from pyclip2playlist.logger_setup import configure_logger

from .clipboard_utils import load_clipboard
from .song_extractor import extract_songs
from .models import Song, SongCollection
from . import gui_helpers  # Added helper import

configure_logger()  # Configure logger once

logger = logging.getLogger(__name__)

def resource_path(relative_path: str) -> str:
    """Return absolute path to a resource; works for development and PyInstaller.
    
    Args:
        relative_path: The relative resource path.
        
    Returns:
        str: Absolute path to the resource.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class PyClip2PlaylistGUI:
    """Main GUI application class."""
    
    def __init__(self) -> None:
        """Initialize the GUI application."""
        self.songs = SongCollection()
        self.setup_window()
        self.setup_styles()
        gui_helpers.create_menu(self)
        gui_helpers.create_layout(self)
        gui_helpers.create_status_bar(self)
    
    def setup_window(self):
        """Configure main window properties."""
        self.root = tk.Tk()
        self.root.title("PyClip2Playlist")
        self.root.geometry("900x600")
        try:
            # When installed as package
            icon_path = resource_path('resources/app.ico')
            if not os.path.exists(icon_path):
                # When run directly from the repository
                icon_path = resource_path('pyclip2playlist/resources/app.ico')
            self.root.iconbitmap(icon_path)
        except Exception:
            # Skip icon setup if not found.
            pass
        self.root.minsize(800, 500)
    
    def setup_styles(self):
        """Configure ttk styles."""
        style = ttk.Style(self.root)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("TFrame", padding=10)
        style.configure("TLabel", padding=5)
        style.configure("TButton", padding=5)
    
    def refresh_clipboard(self):
        """Refresh the clipboard content displayed in the text widget."""
        content = load_clipboard()
        self.clipboard_text.config(state='normal')
        self.clipboard_text.delete("1.0", tk.END)
        self.clipboard_text.insert(tk.END, content)
        self.status_var.set("Clipboard updated.")
    
    def extract_button(self):
        """Extract songs from the clipboard content and update the table."""
        content = self.clipboard_text.get("1.0", tk.END)
        extracted = extract_songs(content)
        self.songs = SongCollection()
        for song_dict in extracted:
            self.songs.add_song(Song(title=song_dict['TITLE'],
                                   artist=song_dict['ARTIST']))
        self.update_table()
        self.status_var.set(f"{len(self.songs)} song(s) extracted.")
    
    def update_table(self):
        """Refresh the table view with the current list of songs."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for song_dict in self.songs.to_dict_list():
            self.tree.insert('', tk.END, values=(song_dict['TITLE'],
                                               song_dict['ARTIST']))
    
    def on_right_click(self, event):
        """Display the context menu for deletion upon right-click."""
        row = self.tree.identify_row(event.y)
        if row:
            self.tree.selection_set(row)
            self.tree.focus(row)
            self.context_menu.tk_popup(event.x_root, event.y_root)
    
    def remove_selected_item(self):
        """Remove the selected song from the table."""
        item = self.tree.focus()
        if not item:
            messagebox.showinfo("Info", "Please select a song to delete.")
            return
        idx = self.tree.index(item)
        self.songs.remove_song(idx)
        self.tree.delete(item)
        self.status_var.set("Entry deleted.")
    
    def on_double_click(self, event):
        """Allow in-place editing of a cell on double-click."""
        if self.tree.identify("region", event.x, event.y) != "cell":
            return
            
        column = self.tree.identify_column(event.x)
        row = self.tree.identify_row(event.y)
        if not row:
            return
            
        x, y, width, height = self.tree.bbox(row, column)
        cell_value = self.tree.set(row, column)
        
        edit_entry = tk.Entry(self.tree)
        edit_entry.place(x=x, y=y, width=width, height=height)
        edit_entry.insert(0, cell_value)
        edit_entry.focus_set()
        
        def save_edit(event=None):
            new_value = edit_entry.get()
            self.tree.set(row, column, new_value)
            edit_entry.destroy()
            
            idx = self.tree.index(row)
            vals = self.tree.item(row)['values']
            if column == "#1":
                new_song = Song(title=new_value, artist=vals[1])
            elif column == "#2":
                new_song = Song(title=vals[0], artist=new_value)
            else:
                new_song = Song(title=vals[0], artist=vals[1])
                
            self.songs.update_song(idx, new_song)
            self.status_var.set("Entry updated.")
        
        edit_entry.bind("<Return>", save_edit)
        edit_entry.bind("<FocusOut>", lambda e: save_edit())
    
    def save_csv_dialog(self):
        """Show dialog to save the song list as a CSV file."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Save CSV as"
        )
        if filename:
            self.save_csv(filename)
    
    def save_csv(self, filename: str):
        """Save the song list to a CSV file.
        
        Args:
            filename: Path to save the CSV file.
        """
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['TITLE', 'ARTIST'])
                writer.writeheader()
                writer.writerows(self.songs.to_dict_list())
            self.status_var.set(f"Saved to {filename}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error saving CSV: {e}")
            return False
    
    def run(self) -> None:
        """Run the GUI and handle unexpected errors."""
        try:
            self.root.mainloop()
        except Exception as e:
            logger.exception("An error occurred during GUI execution:")
            raise

if __name__ == '__main__':
    app = PyClip2PlaylistGUI()
    app.run()
