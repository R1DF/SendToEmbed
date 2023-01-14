# Imports
import requests
import threading
import webbrowser
from tkinter import Tk, Toplevel, Label, Frame, Text, Scrollbar, Button, messagebox
from .notifier import Notifier


# Class code
class UpdateCheck:
    def __init__(self, master: Tk):
        self.master = master
        self.master.currently_checking_updates = True

        thread = threading.Thread(target=self.begin)
        thread.start()

    def begin(self):
        # Connecting to version check
        try:
            version_data = requests.get("https://r1df.github.io/version_check.json").json()["ste"]
            latest_version = version_data["v"]
            version_note = version_data["note"]

            if self.master.version != latest_version:
                Notifier(self.master, latest_version, version_note)

            else:
                messagebox.showinfo("No updates detected", "You're on the latest version. No updates needed.")
                self.master.currently_checking_updates = False

        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "Couldn't connect to the internet. Do you have an internet connection?")
            return

