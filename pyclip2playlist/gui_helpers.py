import tkinter as tk
from tkinter import ttk, scrolledtext
import webbrowser
from .clipboard_utils import load_clipboard

SPOTIFY_IMPORTER_URL = "https://nickwanders.com/projects/ng-spotify-importer/"

def open_spotify_importer():
    """Open the Spotify Importer website in the default browser."""
    webbrowser.open(SPOTIFY_IMPORTER_URL)

def create_menu(gui):
    """Create the application menu bar."""
    gui.menubar = tk.Menu(gui.root)
    
    file_menu = tk.Menu(gui.menubar, tearoff=0)
    file_menu.add_command(label="Save CSV...", command=gui.save_csv_dialog)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=gui.root.quit)
    gui.menubar.add_cascade(label="File", menu=file_menu)
    
    spotify_menu = tk.Menu(gui.menubar, tearoff=0)
    spotify_menu.add_command(label="Open Spotify Importer", command=open_spotify_importer)
    gui.menubar.add_cascade(label="Spotify", menu=spotify_menu)
    
    gui.root.config(menu=gui.menubar)

def create_layout(gui):
    """Set up the main application layout."""
    gui.paned = ttk.PanedWindow(gui.root, orient=tk.HORIZONTAL)
    gui.paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    create_left_frame(gui)
    create_right_frame(gui)

def create_left_frame(gui):
    """Create the left pane with clipboard content and controls."""
    left_frame = ttk.Frame(gui.paned)
    gui.paned.add(left_frame, weight=1)
    clipboard_label = ttk.Label(left_frame, text="Clipboard Content:")
    clipboard_label.pack(anchor=tk.W)
    gui.clipboard_text = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, height=15, font=('TkDefaultFont', 10))
    gui.clipboard_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
    # Configure text widget for UTF-8
    gui.clipboard_text.configure(font=('TkDefaultFont', 10))
    content = load_clipboard()
    if isinstance(content, bytes):
        content = content.decode('utf-8', errors='replace')
    else:
        content = content.encode('utf-8', errors='replace').decode('utf-8')
    gui.clipboard_text.insert(tk.END, content)
    gui.clipboard_text.config(state='normal')
    clipboard_buttons = ttk.Frame(left_frame)
    clipboard_buttons.pack(fill=tk.X, pady=5)
    ttk.Button(clipboard_buttons, text="Refresh Clipboard",
                 command=gui.refresh_clipboard).pack(side=tk.LEFT, padx=5)
    ttk.Button(clipboard_buttons, text="Extract Songs",
                 command=gui.extract_button).pack(side=tk.LEFT, padx=5)

def create_right_frame(gui):
    """Create the right pane with the songs table."""
    right_frame = ttk.Frame(gui.paned)
    gui.paned.add(right_frame, weight=3)
    table_label = ttk.Label(right_frame, text="Extracted Songs (Title | Artist):")
    table_label.pack(anchor=tk.W)
    tree_frame = ttk.Frame(right_frame)
    tree_frame.pack(fill=tk.BOTH, expand=True)
    # Configure style for treeview
    style = ttk.Style()
    style.configure("Treeview", font=('TkDefaultFont', 10))
    style.configure("Treeview.Heading", font=('TkDefaultFont', 10, 'bold'))
    
    gui.tree = ttk.Treeview(tree_frame, columns=('TITLE', 'ARTIST'),
                           show='headings', selectmode='browse', style="Treeview")
    gui.tree.heading('TITLE', text='Title')
    gui.tree.heading('ARTIST', text='Artist')
    gui.tree.column('TITLE', anchor='w', width=300)
    gui.tree.column('ARTIST', anchor='w', width=200)
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=gui.tree.yview)
    gui.tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side='right', fill='y')
    gui.tree.pack(fill=tk.BOTH, expand=True)
    save_csv_frame = ttk.Frame(right_frame)
    save_csv_frame.pack(fill=tk.X, pady=5)
    ttk.Button(save_csv_frame, text="Save CSV",
                 command=gui.save_csv_dialog).pack(side=tk.RIGHT, padx=5)
    gui.tree.bind("<Button-3>", gui.on_right_click)
    gui.tree.bind("<Double-1>", gui.on_double_click)
    gui.context_menu = tk.Menu(gui.root, tearoff=0)
    gui.context_menu.add_command(label="Delete Song", command=gui.remove_selected_item)

def create_status_bar(gui):
    """Create the status bar."""
    gui.status_var = tk.StringVar()
    gui.status_var.set("Ready.")
    gui.status_bar = ttk.Label(gui.root, textvariable=gui.status_var,
                               relief=tk.SUNKEN, anchor='w')
    gui.status_bar.pack(fill=tk.X, padx=10, pady=2, side=tk.BOTTOM)
