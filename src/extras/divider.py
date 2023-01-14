# Imports
from tkinter import Tk, Canvas


# Class code
class Divider:
    """Creates a small Canvas that draws a line over the X axis of the screen."""
    def __init__(self, master: Tk, window_width):
        self.master = master
        self.canvas = Canvas(self.master, height=5, width=window_width)
        self.canvas.pack()
        self.canvas.create_line(3, 3, window_width - 1, 3, fill="BLACK")

