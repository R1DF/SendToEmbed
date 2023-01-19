"""
Send to Embed (from R1DF)
Allows its user to send an embed to a channel through the use of a webhook.
"""

# Imports
import os
import webbrowser
import toml
import tomllib
from tkinter import Tk, Frame, Text, Label, Entry, Button, IntVar, messagebox, PhotoImage, Checkbutton, Menu, filedialog
from tkinter.ttk import Scrollbar
from extras import *
from tkinter.colorchooser import askcolor
from discord_webhook import DiscordWebhook, DiscordEmbed
from requests.exceptions import ConnectionError
from threading import Thread

# Constants
BG_COLOUR = "#E8E8E8"
WIDTH, HEIGHT = 540, 740


# Building GUI class
class SendToEmbed(Tk):
    def __init__(self):
        # Window initialization
        super().__init__()
        self.REPOSITORY_LINK = "https://github.com/R1DF/SendToEmbed"
        self.author_name = ""
        self.author_icon = ""
        self.author_url = ""
        self.thumbnail_path = ""
        self.thumbnail_filename = ""
        self.version = "1.0.0"
        self.current_colour_rgb = (145, 145, 145)
        self.current_colour_hex = "#919191"
        self.has_author_query = False
        self.has_about_toplevel = False
        self.currently_checking_updates = False
        self.contains_timestamp = IntVar()
        self.title("Send to Embed")

        # Window setup (Widgets come after)
        self.config(bg=BG_COLOUR)
        self.resizable(False, False)

        # Webhook URL input
        self.webhook_url_label = Label(text="Webhook URL:", bg=BG_COLOUR)
        self.webhook_url_label.pack()

        self.webhook_url_entry = Entry()
        self.webhook_url_entry.insert(0, "https://discord.com/api/webhooks/")
        self.webhook_url_entry.pack(fill="x")

        Divider(self, WIDTH)

        # Webhook username input
        self.webhook_username_label = Label(text="Webhook Username:", bg=BG_COLOUR)
        self.webhook_username_label.pack()

        self.webhook_username_entry = Entry(width=50)
        self.webhook_username_entry.pack()

        # Webhook title input
        self.webhook_title_label = Label(text="Title:", bg=BG_COLOUR)
        self.webhook_title_label.pack()

        self.webhook_title_entry = Entry(width=50)
        self.webhook_title_entry.pack()

        # Webhook description input
        self.webhook_description_label = Label(text="Description:", bg=BG_COLOUR)
        self.webhook_description_label.pack()

        self.webhook_description_frame = Frame(bg=BG_COLOUR)
        self.webhook_description_frame.pack()

        self.webhook_description_text = Text(self.webhook_description_frame, width=50, height=8, font="Calibri 10")
        self.webhook_description_text.grid(row=0, column=0)

        self.webhook_description_scrollbar = Scrollbar(self.webhook_description_frame, orient="vertical",
                                                       command=self.webhook_description_text.yview)
        self.webhook_description_scrollbar.grid(row=0, column=1, sticky="ns")

        self.webhook_description_text.config(yscrollcommand=self.webhook_description_scrollbar.set)

        # Webhook author and thumbnail input
        self.author_button = Button(text="Change author", command=self.change_author, bg=BG_COLOUR)
        self.author_button.pack(pady=5)

        self.thumbnail_frame = Frame(bg=BG_COLOUR)
        self.thumbnail_frame.pack()

        self.thumbnail_label = Label(self.thumbnail_frame, text="Thumbnail: None", bg=BG_COLOUR)
        self.thumbnail_label.grid(row=0, column=0)

        self.select_thumbnail_button = Button(self.thumbnail_frame, text="Select", command=self.change_thumbnail)
        self.select_thumbnail_button.grid(row=0, column=1)

        Divider(self, WIDTH)

        # Embed fields
        self.fields_extended_listbox = ExtendedListbox(self, ["field", "fields"], 1)
        Divider(self, WIDTH)

        # Images
        self.files_extended_listbox = ExtendedListbox(self, ["file", "files"], 2)
        Divider(self, WIDTH)

        # Footer, timestamp, colour
        self.footer_label = Label(text="Footer:", bg=BG_COLOUR)
        self.footer_label.pack()

        self.footer_entry = Entry(width=50)
        self.footer_entry.pack()

        self.timestamp_checkbutton = Checkbutton(text="Add timestamp", variable=self.contains_timestamp, bg=BG_COLOUR)
        self.timestamp_checkbutton.pack()

        self.colour_frame = Frame(bg=BG_COLOUR)
        self.colour_frame.pack()

        self.colour_label = Label(self.colour_frame, text="Embed colour:", bg=BG_COLOUR)
        self.colour_label.grid(row=0, column=0)

        self.colour_button = Button(self.colour_frame, text="Select", command=self.change_colour)
        self.colour_button.grid(row=0, column=1)

        self.colour_preview_label = Label(self.colour_frame, text=self.current_colour_hex, fg=self.current_colour_hex,
                                          bg=BG_COLOUR)
        self.colour_preview_label.grid(row=0, column=2)

        # Button to send webhook
        self.send_button = Button(text="Send", width=15, font="Arial 15", command=self.begin_send_embed_thread)
        self.send_button.pack(side="bottom", pady=5)

        # Creating the menu bar and linking to self
        self.menu_bar = Menu()
        self.config(menu=self.menu_bar)

        # Embed menu
        self.embed_menu = Menu(self.menu_bar, tearoff=0)
        self.embed_menu.add_command(label="Modify author", command=self.change_author)
        self.embed_menu.add_command(label="Modify colour", command=self.change_colour)
        self.embed_menu.add_command(label="Modify thumbnail", command=self.change_thumbnail)
        self.embed_menu.add_separator()
        self.embed_menu.add_command(label="Add field", command=self.fields_extended_listbox.make_adder)
        self.embed_menu.add_command(label="Delete selected field", command=self.fields_extended_listbox.delete_element)
        self.embed_menu.add_command(label="Edit selected field", command=self.fields_extended_listbox.make_editor)
        self.embed_menu.add_separator()
        self.embed_menu.add_command(label="Add file", command=self.files_extended_listbox.make_adder)
        self.embed_menu.add_command(label="Delete selected file", command=self.files_extended_listbox.delete_element)
        self.embed_menu.add_command(label="Edit selected file", command=self.files_extended_listbox.make_editor)
        # self.embed_menu.add_separator()  TODO later version only!
        # self.embed_menu.add_command(label="Preview code for Python")

        # Templates menu
        self.templates_menu = Menu(self.menu_bar, tearoff=0)
        self.templates_menu.add_command(label="Load from template", command=self.load_template)
        self.templates_menu.add_command(label="Save as template", command=self.save_to_template)

        # Help menu
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About Send to Embed", command=self.make_about_toplevel)
        self.help_menu.add_command(label="Open repository link",
                                   command=lambda: webbrowser.open_new_tab(self.REPOSITORY_LINK))
        self.help_menu.add_command(label="Check for updates", command=self.check_for_updates)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="Version:", accelerator=f"V{self.version}")

        # Adding previous sub-menus to self.menu_bar
        self.menu_bar.add_cascade(label="Embed", menu=self.embed_menu)
        self.menu_bar.add_cascade(label="Templates", menu=self.templates_menu)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

    def reset(self):
        self.webhook_url_entry.delete(0, "end")
        self.webhook_title_entry.delete(0, "end")
        self.webhook_username_entry.delete(0, "end")

        self.author_name = ""
        self.author_icon = ""
        self.author_url = ""

        self.thumbnail_path = ""
        self.thumbnail_label.config(text="Thumbnail: None")

        self.webhook_description_text.delete(1.0, "end")
        self.footer_entry.delete(0, "end")
        self.contains_timestamp.set(0)

        self.fields_extended_listbox.contains = []
        self.fields_extended_listbox.container_listbox.delete(0, "end")

        self.files_extended_listbox.contains = []
        self.files_extended_listbox.container_listbox.delete(0, "end")

        self.current_colour_rgb, self.current_colour_hex = (232, 232, 232), "919191"

    def load_template(self):
        template = filedialog.askopenfilename(
            initialdir=os.path.join(os.getcwd(), "templates"),
            filetypes=[
                ("TOML files", "*.toml")
            ]
        )

        if template:
            self.reset()

            try:
                # Getting data
                with open(template, "rb") as f:
                    data = tomllib.load(f)

                # Overwriting webhook data
                self.webhook_url_entry.insert("end", data["webhook"]["url"])
                self.webhook_title_entry.insert("end", data["webhook"]["title"])
                self.webhook_username_entry.insert("end", data["webhook"]["username"])

                # Overwriting author data
                self.author_name, self.author_icon, self.author_url = data["author"]["name"], data["author"]["icon"], \
                    data["author"]["url"]

                # Overwriting embed data
                self.webhook_description_text.insert("end", data["embed"]["description"])
                self.footer_entry.insert("end", data["embed"]["footer"])
                self.contains_timestamp.set(int(data["embed"]["timestamp"]))
                self.current_colour_hex = data["embed"]["colour"]

                ## HEX to RGB conversion
                hex_code = self.current_colour_hex[1:]
                hex_code_length = len(hex_code)
                self.current_colour_rgb = tuple(int(hex_code[i:i + hex_code_length // 3], 16) for i in
                                                range(0, hex_code_length, hex_code_length // 3))

                # Adding fields and files
                for field in data["embed"]["fields"]:
                    self.fields_extended_listbox.add_element({
                        "title": field[0],
                        "description": field[1],
                        "inline": field[2]
                    })

                for file in data["embed"]["files"]:
                    self.files_extended_listbox.add_element({
                        "url": file[0],
                        "filename": file[1],
                        "extension": file[2]
                    })

            except toml.TomlDecodeError:
                messagebox.showerror("Error", "The template file was unable to be read.")

            # except Exception as e:
            #     messagebox.showerror("Error", f"Couldn't fully load template. [{e}]")

    def save_to_template(self):
        # Choosing location (not default)
        path = filedialog.asksaveasfilename(
            defaultextension=".toml",
            filetypes=[
                ("TOML file", "*.toml")
            ],
            initialdir=os.path.join(os.getcwd(), "templates")
        )
        if path:
            # Creating dict
            template_data = {
                "webhook": {},
                "author": {},
                "embed": {}
            }

            # Saving webhook data
            template_data["webhook"]["url"] = self.webhook_url_entry.get().strip()
            template_data["webhook"]["title"] = self.webhook_title_entry.get().strip()
            template_data["webhook"]["username"] = self.webhook_username_entry.get().strip()

            # Saving author data
            template_data["author"]["name"] = self.author_name
            template_data["author"]["icon"] = self.author_icon
            template_data["author"]["url"] = self.author_url

            # Saving embed content
            template_data["embed"]["description"] = self.webhook_description_text.get(1.0, "end").strip()
            template_data["embed"]["footer"] = self.footer_entry.get().strip()
            template_data["embed"]["timestamp"] = bool(self.contains_timestamp.get())
            template_data["embed"]["fields"] = []
            template_data["embed"]["files"] = []
            template_data["embed"]["colour"] = self.current_colour_hex

            # Adding fields
            for field in self.fields_extended_listbox.contains:
                template_data["embed"]["fields"].append(
                    [field["title"], field["description"], field["inline"]]
                )

            # Adding files
            for file in self.files_extended_listbox.contains:
                template_data["embed"]["files"].append(
                    [file["url"], file["filename"], file["extension"]]
                )

            # Saving
            with open(path, "w") as file:
                toml.dump(template_data, file)

    def check_for_updates(self):
        if not self.currently_checking_updates:
            UpdateCheck(self)

    def begin_send_embed_thread(self):
        thread = Thread(target=self.send_embed)  # mfw threads can't be restarted
        thread.start()

    def hex_to_rgb(self, hex_code):
        rgb = []
        for i in range(0, 5, 2):
            rgb.append(int(hex_code[i:i + 1]))
        return tuple(rgb)

    def change_colour(self):
        colors = askcolor()
        if colors[0] is not None:
            self.current_colour_rgb, self.current_colour_hex = colors
            self.current_colour_hex = self.current_colour_hex.upper()
            self.colour_preview_label.config(text=self.current_colour_hex, fg=self.current_colour_hex)

    def change_author(self):
        if not self.has_author_query:
            AuthorEditor(self, self.author_name, self.author_icon, self.author_url)

    def make_about_toplevel(self):
        if not self.has_about_toplevel:
            AboutToplevel(self)

    def change_thumbnail(self):
        thumbnail_path = filedialog.askopenfilename(
            title="Select image",
            filetypes=(
                ("PNG image", "*.png"),
                ("JPEG image", "*.jpg")
            )
        )

        if not thumbnail_path:
            self.thumbnail_path = self.thumbnail_filename = ""
            self.thumbnail_label.config(text="Thumbnail: None")
            return

        self.thumbnail_path = thumbnail_path
        file_name = self.thumbnail_path.split("/")[-1]
        self.thumbnail_filename = file_name
        if len(file_name) > 30:
            file_name = file_name[:30] + "..."
        self.thumbnail_label.config(text=f"Thumbnail: {file_name}")

    def send_embed(self):
        self.send_button.config(state="disabled")
        webhook_url = self.webhook_url_entry.get().strip()
        if not webhook_url:
            messagebox.showerror("Error", "Please enter a webhook URL.")
            self.send_button.config(state="normal")
            return

        elif not (webhook_url.lower().startswith(
                "https://discord.com/api/webhooks/") or webhook_url.lower().startswith(
            "http://discord.com/api/webhooks/")):
            messagebox.showerror("Error", "Please enter a valid webhook URL.")
            self.send_button.config(state="normal")
            return

        # Getting other data
        username = self.webhook_username_entry.get().strip()
        title = self.webhook_title_entry.get().strip()
        description = self.webhook_description_text.get(1.0, "end").strip()
        fields = self.fields_extended_listbox.contains
        files = self.files_extended_listbox.contains
        footer = self.footer_entry.get().strip()
        thumbnail = self.thumbnail_path

        # Validation
        if not (fields or title or description or footer or title):
            messagebox.showerror("Error", "Please add more entries.")
            self.send_button.config(state="normal")
            return

        # Creating webhook and embed
        webhook = DiscordWebhook(url=webhook_url, username=username)
        embed = DiscordEmbed(color=self.current_colour_hex[1:])
        if title:
            embed.set_title(title)

        if self.author_name and self.author_icon and self.author_url:
            embed.set_author(name=self.author_name, url=self.author_icon, icon_url=self.author_icon)

        if description:
            embed.set_description(description)

        if footer:
            embed.set_footer(text=footer)

        if thumbnail:
            filename = self.thumbnail_filename
            with open(thumbnail, "rb") as file:
                webhook.add_file(file.read(), filename=filename)
            embed.set_thumbnail(url=f"attachment://{filename}")

        for field in fields:
            embed.add_embed_field(name=field["title"], value=field["description"], inline=field["inline"])

        for file in files:
            with open(file["path"], "rb") as file_object:
                webhook.add_file(file=file_object.read(), filename=f"{file['filename']}.{file['extension']}")

        if self.contains_timestamp.get():
            embed.set_timestamp()

        # Sending
        try:
            webhook.add_embed(embed)
            response = webhook.execute()

            if (status_code := response.status_code) != 200:
                error_message = response.json()["message"]
                messagebox.showerror(f"Error {status_code}",
                                     f"The webhook failed to execute with an HTTP Error {status_code} ({error_message[5:]}).")
            else:
                messagebox.showinfo("Done", "Webhook successfully sent.")

        except ConnectionError:
            messagebox.showerror("Error", "A connection error occurred. Are you connected to the internet?")

        finally:
            self.send_button.config(state="normal")


if __name__ == "__main__":
    app = SendToEmbed()
    if os.path.exists(icon_path := (os.path.join(
            os.getcwd(), "icon", "sendtoembed_icon_32x32.png"
    ))):
        app.iconphoto(True, PhotoImage(file=icon_path))
    app.mainloop()
