# Imports
import os
import platform
import subprocess
import webbrowser
from tkinter import Tk, Toplevel, Frame, Label, Button, PhotoImage
from . import Divider


# Class code
class AboutToplevel(Toplevel):
    def __init__(self, master: Tk):
        self.master = master
        self.master.has_about_toplevel = True
        super().__init__(self.master)
        self.title("About SendToEmbed")
        self.resizable(False, False)

        # GUI
        self.icon = PhotoImage(file=os.path.join(os.getcwd(), "icon", "sendtoembed_icon_64x64.png"))
        self.icon_label = Label(self, image=self.icon)
        self.icon_label.pack()

        self.about_label = Label(self, text="About SendToEmbed", font="Calibri 15")
        self.about_label.pack()

        for prompt in [  # I love underloops
            "Made by R1DF with Python.",
            "Webhooks and embeds implemented with lovvskillz's (GitHub) discord_webhook module.",
            f"Version: {self.master.version}"
        ]:
            label = Label(self, text=prompt)
            label.pack()

        Divider(self, 565)

        self.buttons_frame = Frame(self)
        self.buttons_frame.pack(side="bottom")

        self.open_repository_button = Button(self.buttons_frame, text="Open Repository",
                                             command=lambda: webbrowser.open_new_tab(self.master.REPOSITORY_LINK))
        self.open_repository_button.grid(row=0, column=0, padx=5, pady=5)

        if platform.system() == "Windows":
            self.view_templates_button = Button(self.buttons_frame, text="View Templates", command=self.view_templates)
            self.view_templates_button.grid(row=0, column=1, padx=5, pady=5)

        # Exit handling
        self.protocol("WM_DELETE_WINDOW", self.handle_quit)

    def view_templates(self):
        path = os.path.join(
            os.getcwd(), "templates"
        )
        subprocess.Popen("explorer /open, \"" + path + "\"")

    def handle_quit(self):
        self.master.has_about_toplevel = False
        self.destroy()
