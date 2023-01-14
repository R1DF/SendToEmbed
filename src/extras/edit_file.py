# Imports
from tkinter import Tk, Toplevel, Frame, Label, Entry, Button, messagebox, filedialog


# Class code
class FileEditor(Toplevel):
    def __init__(self, master: Tk, listbox_master, original_data, original_data_index):
        # Initialization
        self.master = master
        self.listbox_master = listbox_master
        self.original_data = original_data
        self.original_data_index = original_data_index
        super().__init__(self.master)
        self.title("Edit File")
        self.resizable(False, False)

        # GUI
        self.file_frame = Frame(self)
        self.file_frame.pack()

        self.file_path_label = Label(self.file_frame, text="File Path:")
        self.file_path_label.grid(row=0, column=0)

        self.file_path_entry = Entry(self.file_frame, width=60)
        self.file_path_entry.insert("end", self.original_data["path"])
        self.file_path_entry.config(state="disabled")
        self.file_path_entry.grid(row=0, column=1)

        self.browse_button = Button(self.file_frame, text="Browse", command=self.browse)
        self.browse_button.grid(row=0, column=2)

        self.filename_label = Label(self.file_frame, text="Filename:")
        self.filename_label.grid(row=1, column=0)

        self.filename_entry = Entry(self.file_frame, width=60)
        self.filename_entry.grid(row=1, column=1)
        self.filename_entry.insert("end", self.original_data["filename"])

        self.save_button = Button(self, text="Save", command=self.edit)
        self.save_button.pack()

        self.protocol("WM_DELETE_WINDOW", self.handle_quit)

    def browse(self):
        dialog = filedialog.askopenfilename(
            title="Select file",
            filetypes=(
                ("PNG images", "*.png"),
                ("JPEG images", "*.jpg"),
                ("GIF images", "*.gif"),
                ("MP3 sounds", "*.mp3"),
                ("WAV sounds", "*.wav"),
                ("MP4 videos", "*.mp4"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            )
        )

        if not dialog:
            return

        self.file_path_entry.config(state="normal")
        self.file_path_entry.delete(0, "end")
        self.file_path_entry.insert("end", dialog)
        self.file_path_entry.config(state="disabled")

        self.filename_entry.delete(0, "end")
        self.filename_entry.insert("end", dialog.split("/")[-1].split(".")[0])

    def handle_quit(self):
        self.listbox_master.has_edit_query = False
        self.destroy()

    def edit(self):
        path = self.file_path_entry.get()
        filename = self.filename_entry.get()

        if (not path) or (not filename):
            messagebox.showerror("Error", "Please fill out the entries.")
            return

        if filename in [x["filename"] for x in self.listbox_master.contains] or \
                path in [x["path"] for x in self.listbox_master.contains]:
            messagebox.showerror("Error", "Please ensure that the filename and the path are both unique.")
            return

        for unusable_character in ("/", "\\", ":", "\"", "'", "|", "?", "*", ".", "#"):
            if unusable_character in filename:
                messagebox.showerror("Error", f"The filename cannot contain the {unusable_character} symbol.")
                return

        data = {
            "path": path,
            "filename": filename,
            "extension": path.split(".")[-1]
        }

        self.listbox_master.edit_element(data, self.original_data_index)
        self.handle_quit()

