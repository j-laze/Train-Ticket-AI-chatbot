# import customtkinter as ctk
from customtkinter import *
from tkinter import Listbox


################################|###############################
############################CONSTANTS###########################
################################|###############################

## DEFAULTS:

APPEARANCE_MODE = "dark"
COLOUR_THEME = "dark-blue"
BASE_FONT = "Helvetica"
PADX = 10
PADY = 10

## WINDOW/APP:

WINDOW_WIDTH  = 1600
WINDOW_HEIGHT = 900
APP_GEOMETRY = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
APP_NAME = "Train AI Chatbot"

## FRAME:

FRAME_FILL = "both"
FRAME_EXPAND = True

## HEADER:

HEADER_FONT = (BASE_FONT, 20)
HEADER_PADX = 10
HEADER_PADY = 20

## CONVERSATION:

CONVO_WIDTH  = 1200
CONVO_HEIGHT = 600
MSG_FONT = (BASE_FONT, 12)
BOT_MSG_COLOR = "lightblue"
USR_MSG_COLOR = "lightgreen"


################################|###############################
#############################CLASSES############################
################################|###############################


class Msg(CTkLabel):
    def __init__(self, anchor: str, **kwargs):
        super().__init__(text_color="black", font=MSG_FONT, justify="left", corner_radius=PADX, wraplength=400, padx=PADX, pady=PADY, **kwargs)
        self.pack(anchor=anchor, padx=PADX, pady=PADY)

class UsrMsg(Msg):
    def __init__(self, **kwargs):
        super().__init__(anchor="e", fg_color=USR_MSG_COLOR, **kwargs)

class BotMsg(Msg):
    def __init__(self, **kwargs):
        super().__init__(anchor="w", fg_color=BOT_MSG_COLOR, **kwargs)


class Conversation(CTkScrollableFrame):
    def __init__(self, master: CTkBaseClass, **kwargs):
        super().__init__(master=master, **kwargs)

        self.pack(padx=PADX, pady=PADY)
        self.configure(width=CONVO_WIDTH, height=CONVO_HEIGHT)
        
    def add(self, sent_by: str, text: str):
        UsrMsg(master=self, text=text) if sent_by=="usr" else BotMsg(master=self, text=text)
        self.update_idletasks()
        self._parent_canvas.yview_moveto(1)
