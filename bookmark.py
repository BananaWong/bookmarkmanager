import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from bs4 import BeautifulSoup

def load_bookmarks():
    """Load the bookmarks file and display them in the treeview."""
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            bookmarks_data = file.read()

        soup = BeautifulSoup(bookmarks_data, 'html.parser')
        treeview.delete(*treeview.get_children())  # Clear existing entries
        for bookmark in soup.find_all('a'):
            title = bookmark.text
            url = bookmark.get('href', '')
            treeview.insert('', 'end', values=(title, url))

        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

def remove_selected():
    """Remove the selected bookmarks."""
    selected_items = treeview.selection()
    for item in selected_items:
        treeview.delete(item)

def save_bookmarks():
    """Save the updated bookmarks to a new file."""
    file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('<!DOCTYPE NETSCAPE-Bookmark-file-1>\n')
            file.write('<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n')
            file.write('<TITLE>Bookmarks</TITLE>\n')
            file.write('<H1>Bookmarks</H1>\n')
            file.write('<DL><p>\n')
            for child in treeview.get_children():
                title, url = treeview.item(child)['values']
                file.write(f'    <DT><A HREF="{url}">{title}</A>\n')
            file.write('</DL><p>')
        messagebox.showinfo("Success", "Bookmarks saved successfully!")

# Set up the main window
window = tk.Tk()
window.title("Bookmark Manager")

# Create widgets
btn_load = tk.Button(window, text="Load Bookmarks", command=load_bookmarks)
btn_save = tk.Button(window, text="Save Bookmarks", command=save_bookmarks)
btn_remove = tk.Button(window, text="Remove Selected", command=remove_selected)
entry_file_path = tk.Entry(window, width=50)
treeview = ttk.Treeview(window, columns=('Title', 'URL'), show='headings')
treeview.heading('Title', text='Title')
treeview.heading('URL', text='URL')

# Layout widgets
btn_load.grid(row=0, column=0, padx=5, pady=5)
btn_save.grid(row=1, column=0, padx=5, pady=5)
btn_remove.grid(row=2, column=0, padx=5, pady=5)
entry_file_path.grid(row=0, column=1, padx=5, pady=5)
treeview.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Run the application
window.mainloop()
