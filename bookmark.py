import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from html.parser import HTMLParser
import os

class Bookmark:
    def __init__(self, title, url=None, parent=None):
        self.title = title
        self.url = url
        self.children = []
        self.parent = parent

    def add_child(self, bookmark):
        bookmark.parent = self
        self.children.append(bookmark)

    def is_folder(self):
        return self.url is None

    def __str__(self):
        return self.title if self.is_folder() else f"{self.title} [{self.url}]"

class BookmarkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.root = Bookmark("Root")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = dict(attrs).get('href', '')
            self.stack[-1].add_child(Bookmark(self.last_data, href))
        elif tag == 'h3':
            self.last_data = ''

    def handle_endtag(self, tag):
        if tag == 'dl':
            self.stack.pop()
        elif tag == 'h3':
            folder = Bookmark(self.last_data)
            self.stack[-1].add_child(folder)
            self.stack.append(folder)

    def handle_data(self, data):
        self.last_data = data

    def parse_bookmarks(self, html):
        self.feed(html)
        return self.root

class BookmarkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Bookmark Manager')
        self.geometry('600x400')
        self.create_widgets()
        self.parser = BookmarkParser()
        self.current_folder = None

    def create_widgets(self):
        self.load_button = tk.Button(self, text='Load Bookmarks', command=self.load_bookmarks)
        self.load_button.pack()

        self.back_button = tk.Button(self, text='Back', command=self.go_back)
        self.back_button.pack()

        self.bookmark_listbox = tk.Listbox(self, width=50)
        self.bookmark_listbox.pack()
        self.bookmark_listbox.bind('<Double-1>', self.open_folder)

        self.delete_button = tk.Button(self, text='Delete Selected', command=self.delete_selected)
        self.delete_button.pack()

        self.save_button = tk.Button(self, text='Save Bookmarks', command=self.save_bookmarks)
        self.save_button.pack()

    def load_bookmarks(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                html = file.read()
                self.root = self.parser.parse_bookmarks(html)
                self.current_folder = self.root
                self.populate_listbox()

    def populate_listbox(self):
        self.bookmark_listbox.delete(0, tk.END)
        for item in self.current_folder.children:
            self.bookmark_listbox.insert(tk.END, item)

    def open_folder(self, event):
        selected_index = self.bookmark_listbox.curselection()[0]
        selected_item = self.current_folder.children[selected_index]
        if selected_item.is_folder():
            self.current_folder = selected_item
            self.populate_listbox()

    def go_back(self):
        if self.current_folder.parent:
            self.current_folder = self.current_folder.parent
            self.populate_listbox()

    def delete_selected(self):
        selected_indices = self.bookmark_listbox.curselection()
        for i in selected_indices[::-1]:
            del self.current_folder.children[i]
        self.populate_listbox()

    def save_bookmarks(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.html')
        if file_path:
            # TODO: Convert self.root to HTML and write to file
            pass

if __name__ == '__main__':
    app = BookmarkApp()
    app.mainloop()
