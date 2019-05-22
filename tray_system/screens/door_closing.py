import os
from tkinter import Label, Frame


class DoorClosing(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        label = Label(self, text="Closing doors!")
        label.pack(side="top", fill="x", pady=10)


