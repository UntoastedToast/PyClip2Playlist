import csv
import os
import sys
import pyperclip
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from patterns import patterns

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

songs = []  # List to store extracted songs

def load_clipboard():
    """Return the current content of the system clipboard."""
    return pyperclip.paste()

def fallback_extraction(line):
    """Extract title and artist using simple heuristics if regex patterns don't match."""
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
        artist = line[index + 4:].strip(" :;-")
        if title and artist:
            return title, artist

    return None, None

def extract_songs(text):
    """
    Extract songs (title and artist) from text.
    Tries regex patterns first; if none match, falls back to heuristic extraction.
    If all methods fail, uses the entire line as the title with "Unknown" artist.
    """
    extracted = []
    for line in text.splitlines():
        original_line = line
        line = line.strip()
        if not line:
            continue

        matched = False
        for pattern in patterns:
            match = pattern.match(line)
            if match:
                title = match.group('track').strip()
                artist = match.group('artist').strip()
                extracted.append({'TITLE': title, 'ARTIST': artist})
                matched = True
                break

        if not matched:
            title, artist = fallback_extraction(line)
            if title and artist:
                extracted.append({'TITLE': title, 'ARTIST': artist})
                matched = True

        if not matched:
            extracted.append({'TITLE': line, 'ARTIST': "Unknown"})
            print("Fallback: Using entire line as title:", original_line)

    return extracted

def save_csv(song_list, filename='playlist.csv'):
    """Save the song list to a CSV file."""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['TITLE', 'ARTIST']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for song in song_list:
                writer.writerow(song)
        return True
    except Exception as e:
        print("Error saving CSV:", e)
        return False

# Initialize main application window
root = tk.Tk()
root.title("PyClip2Playlist")
root.geometry("900x600")
root.iconbitmap(resource_path('app.ico'))
root.minsize(800, 500)

# Apply a modern theme if available
style = ttk.Style(root)
if "clam" in style.theme_names():
    style.theme_use("clam")
style.configure("TFrame", padding=10)
style.configure("TLabel", padding=5)
style.configure("TButton", padding=5)

# Setup menu bar with file options
menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(
    label="Save CSV...", 
    command=lambda: save_csv(
        songs, 
        filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Save CSV as"
        )
    )
)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)
root.config(menu=menubar)

# Create a horizontal paned window for layout
paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Left frame: Clipboard content and extraction controls
left_frame = ttk.Frame(paned)
paned.add(left_frame, weight=1)

clipboard_label = ttk.Label(left_frame, text="Clipboard Content:")
clipboard_label.pack(anchor=tk.W)
clipboard_text = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, height=15)
clipboard_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
clipboard_text.insert(tk.END, load_clipboard())
clipboard_text.config(state='normal')

clipboard_buttons = ttk.Frame(left_frame)
clipboard_buttons.pack(fill=tk.X, pady=5)

def refresh_clipboard():
    """Refresh the clipboard content displayed in the text widget."""
    content = load_clipboard()
    clipboard_text.config(state='normal')
    clipboard_text.delete("1.0", tk.END)
    clipboard_text.insert(tk.END, content)
    status_var.set("Clipboard updated.")

def extract_button():
    """Extract songs from clipboard content and update the table."""
    global songs
    content = clipboard_text.get("1.0", tk.END)
    songs = extract_songs(content)
    update_table()
    status_var.set(f"{len(songs)} song(s) extracted.")

ttk.Button(clipboard_buttons, text="Refresh Clipboard", command=refresh_clipboard).pack(side=tk.LEFT, padx=5)
ttk.Button(clipboard_buttons, text="Extract Songs", command=extract_button).pack(side=tk.LEFT, padx=5)

# Right frame: Display extracted songs in a table
right_frame = ttk.Frame(paned)
paned.add(right_frame, weight=3)

table_label = ttk.Label(right_frame, text="Extracted Songs (Title | Artist):")
table_label.pack(anchor=tk.W)

tree_frame = ttk.Frame(right_frame)
tree_frame.pack(fill=tk.BOTH, expand=True)

columns = ('TITLE', 'ARTIST')
tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
tree.heading('TITLE', text='Title')
tree.heading('ARTIST', text='Artist')
tree.column('TITLE', anchor='w')
tree.column('ARTIST', anchor='w')

vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
vsb.pack(side='right', fill='y')
tree.pack(fill=tk.BOTH, expand=True)

def on_right_click(event):
    """Show context menu for deletion on right-click."""
    row = tree.identify_row(event.y)
    if row:
        tree.selection_set(row)
        tree.focus(row)
        context_menu.tk_popup(event.x_root, event.y_root)

def remove_selected_item():
    """Delete the selected song from the table and update the songs list."""
    global songs
    item = tree.focus()
    if not item:
        messagebox.showinfo("Info", "Please select a song to delete.")
        return
    tree.delete(item)
    new_songs = []
    for child in tree.get_children():
        vals = tree.item(child)['values']
        if len(vals) >= 2:
            new_songs.append({'TITLE': vals[0], 'ARTIST': vals[1]})
    songs = new_songs
    status_var.set("Entry deleted.")

def on_double_click(event):
    """Allow in-place editing of a cell on double-click."""
    if tree.identify("region", event.x, event.y) != "cell":
        return
    column = tree.identify_column(event.x)
    row = tree.identify_row(event.y)
    if not row:
        return
    x, y, width, height = tree.bbox(row, column)
    cell_value = tree.set(row, column)
    edit_entry = tk.Entry(tree)
    edit_entry.place(x=x, y=y, width=width, height=height)
    edit_entry.insert(0, cell_value)
    edit_entry.focus_set()

    def save_edit(event=None):
        new_value = edit_entry.get()
        tree.set(row, column, new_value)
        edit_entry.destroy()
        vals = tree.item(row)['values']
        if column == "#1":
            new_song = {'TITLE': new_value, 'ARTIST': vals[1]}
        elif column == "#2":
            new_song = {'TITLE': vals[0], 'ARTIST': new_value}
        else:
            new_song = {'TITLE': vals[0], 'ARTIST': vals[1]}
        songs[tree.index(row)] = new_song
        status_var.set("Entry updated.")

    edit_entry.bind("<Return>", save_edit)
    edit_entry.bind("<FocusOut>", lambda e: save_edit())

tree.bind("<Button-3>", on_right_click)
tree.bind("<Double-1>", on_double_click)

context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Delete Song", command=remove_selected_item)

def update_table():
    """Refresh the treeview to display the current list of songs."""
    for row in tree.get_children():
        tree.delete(row)
    for song in songs:
        tree.insert('', tk.END, values=(song['TITLE'], song['ARTIST']))

save_csv_frame = ttk.Frame(right_frame)
save_csv_frame.pack(fill=tk.X, pady=5)
ttk.Button(
    save_csv_frame,
    text="Save CSV",
    command=lambda: save_csv(
        songs, 
        filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Save CSV as"
        )
    )
).pack(side=tk.RIGHT, padx=5)

status_var = tk.StringVar()
status_var.set("Ready.")
status_bar = ttk.Label(root, textvariable=status_var, relief=tk.SUNKEN, anchor='w')
status_bar.pack(fill=tk.X, padx=10, pady=2, side=tk.BOTTOM)

root.mainloop()
