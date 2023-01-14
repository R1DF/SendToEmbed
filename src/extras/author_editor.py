# Imports
from tkinter import Toplevel, Frame, Label, Entry, Button


# Class code
class AuthorEditor(Toplevel):
    def __init__(self, master, author_name, author_icon, author_url):
        self.master = master
        super().__init__(master)
        self.title("Webhook Author Editor")
        self.resizable(False, False)

        # GUI
        self.entries_frame = Frame(self)
        self.entries_frame.pack()

        self.author_name_label = Label(self.entries_frame, text="Author name: ")
        self.author_name_label.grid(row=0, column=0)

        self.author_name_entry = Entry(self.entries_frame, width=50)
        self.author_name_entry.grid(row=0, column=1)
        self.author_name_entry.insert("end", author_name)

        self.author_icon_label = Label(self.entries_frame, text="Author icon: ")
        self.author_icon_label.grid(row=1, column=0)

        self.author_icon_entry = Entry(self.entries_frame, width=50)
        self.author_icon_entry.grid(row=1, column=1)
        self.author_icon_entry.insert("end", author_icon)

        self.author_url_label = Label(self.entries_frame, text="Author URL: ")
        self.author_url_label.grid(row=2, column=0)

        self.author_url_entry = Entry(self.entries_frame, width=50)
        self.author_url_entry.grid(row=2, column=1)
        self.author_url_entry.insert("end", author_url)

        self.save_button = Button(self, text="Save", command=self.save)
        self.save_button.pack()

        self.protocol("WM_DELETE_WINDOW", self.handle_quit)

    def handle_quit(self):
        self.master.has_author_query = False
        self.destroy()

    def save(self):
        self.master.author_name = self.author_name_entry.get().strip()
        self.master.author_icon = self.author_icon_entry.get().strip()
        self.master.author_url = self.author_url_entry.get().strip()
        self.handle_quit()

