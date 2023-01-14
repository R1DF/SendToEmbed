# Imports
from tkinter import Tk, Frame, Label, Listbox, Button, messagebox
from tkinter.ttk import Scrollbar  # better Scrollbar
from . import FieldAdder, FieldEditor, FileAdder, FileEditor

# Constants
BG_COLOUR = "#E8E8E8"


# Extended Listbox (for Fields, specifically)
class ExtendedListbox:
    """This class is like ListBox, but it's meant specifically for this app."""

    def __init__(self, master: Tk, element_names: list[str], listbox_type):
        self.master = master
        self.contains = []
        self.has_add_query = False
        self.has_edit_query = False
        self.listbox_type = listbox_type
        self.element_names = element_names  # [image, images] / [field, fields]

        self.introduction_label = Label(self.master, text=f"{self.element_names[1].title()}:")
        self.introduction_label.pack()

        self.outer_container_frame = Frame(self.master, bg=BG_COLOUR)  # Outer: buttons below included
        self.outer_container_frame.pack()

        self.inner_container_frame = Frame(self.outer_container_frame, bg=BG_COLOUR)  # Inner: Only elements
        self.inner_container_frame.pack()

        self.container_listbox = Listbox(self.inner_container_frame, width=50, height=5)
        self.container_listbox.grid(row=0, column=0)

        self.container_scrollbar = Scrollbar(self.inner_container_frame, orient="vertical",
                                             command=self.container_listbox.yview)
        self.container_scrollbar.grid(row=0, column=1, sticky="ns")

        self.container_listbox.config(yscrollcommand=self.container_scrollbar.set)

        self.buttons_frame = Frame(self.outer_container_frame)
        self.buttons_frame.pack()

        self.add_element_button = Button(self.buttons_frame, text="Add", command=self.make_adder)
        self.add_element_button.grid(row=0, column=0)

        self.delete_element_button = Button(self.buttons_frame, text="Delete", command=self.delete_element)
        self.delete_element_button.grid(row=0, column=1)

        self.edit_element_button = Button(self.buttons_frame, text="Edit", command=self.make_editor)
        self.edit_element_button.grid(row=0, column=2)

    def make_adder(self):
        if not self.has_add_query:
            self.has_add_query = True
            if self.listbox_type == 1:
                FieldAdder(self.master, self)
            else:
                FileAdder(self.master, self)

    def add_element(self, data):
        self.contains.append(data)
        if self.listbox_type == 1:
            title = data['title']
            self.container_listbox.insert(
                "end",
                f"{'[INLINE]' if data['inline'] else ''} {title if title else data['description'][:10]}"
            )
        else:
            self.container_listbox.insert("end", f"{data['filename']}.{data['extension']}")

    def delete_element(self):
        curselection = self.container_listbox.curselection()
        if not curselection:
            messagebox.showerror("Error", "Please select an entry to delete.")
            return
        self.container_listbox.delete(curselection)
        self.contains.remove(self.contains[curselection[0]])

    def make_editor(self):
        curselection = self.container_listbox.curselection()
        if not curselection:
            messagebox.showerror("Error", "Please select an entry to edit.")
            return

        if not self.has_edit_query:
            self.has_edit_query = True
            if self.listbox_type == 1:
                FieldEditor(self.master, self, self.contains[curselection[0]], curselection[0])
            else:
                FileEditor(self.master, self, self.contains[curselection[0]], curselection[0])

    def edit_element(self, data, index):
        self.contains[index] = data
        self.container_listbox.delete(index)
        if self.listbox_type == 1:
            title = data["title"]
            self.container_listbox.delete(index)
            self.container_listbox.insert(
                index,
                f"{'[INLINE]' if data['inline'] else ''} {title if title else data['description'][:10]}"
            )
        else:
            self.container_listbox.insert(index, f"{data['filename']}.{data['extension']}")

