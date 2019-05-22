import os
from typing import Dict

import tkinter as tk
from PIL import ImageTk, Image
from .state import State
from core.config import ASSETS_DIR

WIDTH = 450
HEIGHT = 450

HEADER_HEIGHT = 100
STATE_FRAME_HEIGHT = 300

FOODCLOUD_LOGO = "foodcloud.png"
TCD_LOGO = "tcd.jpg"
UNIMORE_LOGO = "unimore.jpg"


class ScreenManager(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.state = State.READY

        self.header = tk.Frame(self, width=WIDTH, height=HEADER_HEIGHT, bg='cyan')
        self.header.grid()

        self.setup_header()

        self.state_frame_container = tk.Frame(self, bg='red', width=WIDTH, height=STATE_FRAME_HEIGHT)
        self.state_frame_container.grid()
        # self.state_frame_container.grid_rowconfigure(0, weight=1)
        # self.state_frame_container.grid_columnconfigure(0, weight=5)

        self.frames_by_state: Dict = {}
        for state in State:
            frame = state.value[0](parent=self.state_frame_container, controller=self)
            frame.grid()
            self.frames_by_state[state] = frame
            break

        self.progress_state(self.state)

    def setup_header(self):
        label: tk.Label = tk.Label(self.header, text="FoodCloud etc")
        label.grid()
        self.render_image(ImageTk.PhotoImage(file=os.path.join(ASSETS_DIR, TCD_LOGO)), col=0)
        # self.render_image(ImageTk.PhotoImage(file=os.path.join(ASSETS_DIR, FOODCLOUD_LOGO)), col=1)
        # self.render_image(ImageTk.PhotoImage(file=os.path.join(ASSETS_DIR, UNIMORE_LOGO)), col=2)


    def render_image(self, img, col=0):
        panel = tk.Label(self.header, image=img)
        panel.grid(column=col)

    def progress_state(self, new_state: State):
        self.state = new_state
        self.frames_by_state[new_state].tkraise()
        self.update()

