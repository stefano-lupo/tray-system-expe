import os
from tkinter import Label, Frame
from ..lib.animated_gif import AnimatedGif
from core.config import ASSETS_DIR

class ReadyScreen(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        label = Label(self, text="Ready for trays!")
        label.pack(side="top", fill="x", pady=10)
        gears = AnimatedGif(self, os.path.join(ASSETS_DIR, 'gears.gif'), 0.04)
        gears.pack()
        gears.start()

