# Imports
import webbrowser
from tkinter import Tk, Toplevel, Label, Frame, Text, Scrollbar, Button, messagebox


# Class code
class Notifier(Toplevel):
    def __init__(self, master, latest_version, version_note):
        self.master = master
        super().__init__(self.master)
        self.title("New version detected!")
        self.resizable(False, False)

        self.version_label = Label(self, text="New version detected!", fg="RED")
        self.version_label.pack()

        self.version_label_2 = Label(self, text=f"Current: {self.master.version}\nLatest: {latest_version}")
        self.version_label_2.pack()

        if version_note:
            self.notes_frame = Frame(self)
            self.notes_frame.pack()
            self.notes_text = Text(self.notes_frame, font="Calibri 10", height=8, width=50)
            self.notes_text.grid(row=0, column=0)
            self.notes_text.insert("end", version_note)
            self.notes_text.config(state="disabled")

            self.notes_scrollbar = Scrollbar(self.notes_frame, orient="vertical",
                                             command=self.notes_text.yview)
            self.notes_scrollbar.grid(row=0, column=1, sticky="ns")
            self.notes_text.config(yscrollcommand=self.notes_scrollbar.set)

        else:
            self.no_note_label = Label(self, text="There are no notes the latest version.")
            self.no_note_label.pack()

        self.where_updates_label = Label(self, text="Versions are available at the repository for SendToEmbed.")
        self.where_updates_label.pack()

        self.get_updates_button = Button(self, text="Open Repository",
                                         command=lambda: webbrowser.open_new_tab(self.master.REPOSITORY_LINK))
        self.get_updates_button.pack()

        self.protocol("WM_DELETE_WINDOW", self.handle_quit)

    def handle_quit(self):
        self.master.currently_checking_updates = False
        self.destroy()

