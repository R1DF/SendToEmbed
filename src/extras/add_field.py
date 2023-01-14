# Imports
from tkinter import Tk, Toplevel, Frame, Label, Entry, Text, Button, Scrollbar, Checkbutton, IntVar, messagebox


# Class code
class FieldAdder(Toplevel):
    def __init__(self, master: Tk, listbox_master):
        # Initialization
        self.master = master
        self.listbox_master = listbox_master
        self.is_inline_intvar = IntVar()
        super().__init__(self.master)
        self.title("Add Field")
        self.resizable(False, False)

        # GUI
        self.title_frame = Frame(self)
        self.title_frame.pack()

        self.title_label = Label(self.title_frame, text="Title:")
        self.title_label.grid(row=0, column=0)

        self.title_entry = Entry(self.title_frame)
        self.title_entry.grid(row=0, column=1)

        self.description_label = Label(self, text="Description:")
        self.description_label.pack()

        self.description_frame = Frame(self)
        self.description_frame.pack()

        self.description_text = Text(self.description_frame, height=10, font="Calibri 10")
        self.description_text.grid(row=0, column=0)

        self.description_scrollbar = Scrollbar(self.description_frame, orient="vertical",
                                               command=self.description_text.yview)
        self.description_scrollbar.grid(row=0, column=1, sticky="ns")
        self.description_text.config(yscrollcommand=self.description_scrollbar.set)

        self.is_inline_checkbutton = Checkbutton(self, text="Inline?", variable=self.is_inline_intvar)
        self.is_inline_checkbutton.pack()

        self.add_field_button = Button(self, text="Add", command=self.add)
        self.add_field_button.pack()

        self.protocol("WM_DELETE_WINDOW", self.handle_quit)

    def handle_quit(self):
        self.listbox_master.has_add_query = False
        self.destroy()

    def add(self):
        data = {
            "title": self.title_entry.get().strip(),
            "description": self.description_text.get(1.0, "end").strip(),
            "inline": bool(self.is_inline_intvar.get())
        }

        if (not data["description"]) and (not data["title"]):
            messagebox.showerror("Error", "Please add a title or a description.")
            return

        self.listbox_master.add_element(data)
        self.handle_quit()

