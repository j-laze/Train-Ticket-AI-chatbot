# import customtkinter as ctk
from customtkinter import *
from tkinter import Listbox


################################|###############################
############################CONSTANTS###########################
################################|###############################

## DEFAULTS:

APPEARANCE_MODE = "dark"
COLOUR_THEME = "dark-blue"
PADX = 10
PADY = 10

## WINDOW/APP:

WINDOW_WIDTH  = 450
WINDOW_HEIGHT = 650
APP_GEOMETRY = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
APP_NAME = "Tinker Trian Chatbot"

## TABVIEW:

TAB_NAMES = [ "Find Best Tickets", "Delay Information" ]

## FRAME:

FRAME_FILL = "both"
FRAME_EXPAND = True

## HEADER:

HEADER_FONT = ("Arial", 20)
HEADER_PADX = 10
HEADER_PADY = 20

## CONVERSATION:

CONVO_WIDTH  = 350
CONVO_HEIGHT = 450
MSG_FONT = ("Arial", 12)
BOT_MSG_COLOR = "lightblue"
USR_MSG_COLOR = "lightgreen"


################################|###############################
#############################CLASSES############################
################################|###############################


class Msg(CTkLabel):
    def __init__(self, anchor: str, **kwargs):
        super().__init__(text_color="black", justify="left", corner_radius=PADX, **kwargs)
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


class App(CTk):
    def __init__(self):
        super().__init__()
        
        self.messages: list[(str, str)] = [] ## [(sent_by, text),...]

        set_appearance_mode(APPEARANCE_MODE)
        set_default_color_theme(COLOUR_THEME)

        self.geometry(APP_GEOMETRY)
        self.title(APP_NAME)
        
        self.frame = CTkFrame(master=self)
        self.frame.pack(fill=FRAME_FILL, expand=FRAME_EXPAND, padx=PADX*3, pady=PADY*3)

        self.header = CTkLabel(master=self.frame, text=APP_NAME, font=HEADER_FONT)
        self.header.pack(pady=(2*PADY, PADY), padx=PADX)
        
        self.conversation = Conversation(master=self.frame)
        
        self.entry = CTkEntry(master=self.frame, placeholder_text="...", width=CONVO_WIDTH+2*PADX)
        self.entry.bind("<Return>", self.send_user_msg)
        self.entry.pack(padx=PADX, pady=PADY)
        
        self.send_bot_msg("INITIAL PROMPT")
        
    def waiting_for_user(self):
        return self.messages[-1][0] == "bot"
    
    def waiting_for_bot(self):
        return not self.waiting_for_user()
        
    def send_user_msg(self, _):
        if self.waiting_for_user():
            self.messages.append(("usr", self.entry.get()))
            self.conversation.add("usr", self.entry.get())
            self.entry.delete(0, "end")
            
    def send_bot_msg(self, msg):
        self.messages.append(("bot", msg))
        self.conversation.add("bot", msg)
