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

WINDOW_WIDTH  = 600
WINDOW_HEIGHT = 600
APP_GEOMETRY = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
APP_NAME = "Tinker Trian"

## TABVIEW:

TAB_NAMES = [ "Find Best Tickets", "Delay Information" ]

## FRAME:

FRAME_FILL = "both"
FRAME_EXPAND = True

## TITLES:

TITLE_FONT = ("Arial", 20)
TITLE_PADX = 10
TITLE_PADY = 20

## CONVERSATION:

CONVO_WIDTH  = 400
CONVO_HEIGHT = 400
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
        self.configure(width=400, height=400)
        
    def add(self, sent_by: str, text: str):
        UsrMsg(master=self, text=text) if sent_by=="usr" else BotMsg(master=self, text=text)


class Tab(CTkFrame):
    def __init__(self, master: CTkBaseClass, title: str, **kwargs):
        super().__init__(master=master, **kwargs)
        
        self.pack(fill=FRAME_FILL, expand=FRAME_EXPAND)
        
        self.title = CTkLabel(master=self, text=title, font=TITLE_FONT)
        self.title.pack(pady=PADY, padx=PADX)

        self.conversation = Conversation(master=self)
        
        self.entry = CTkEntry(master=self, placeholder_text="...")
        self.entry.bind("<Return>", self.send_msg)
        self.entry.pack(padx=PADX, pady=PADY)
        
    def send_msg(self, event):
        self.conversation.add("usr", self.entry.get())
        self.entry.delete(0, "end")


class TabView(CTkTabview):
    def __init__(self, master: CTkBaseClass, **kwargs):
        super().__init__(master=master, **kwargs)
        
        self.pack(padx=PADX, pady=PADY)
        
        self.search_tab = self.add(TAB_NAMES[0])
        self.delay_tab = self.add(TAB_NAMES[1])


class Gui(CTk):
    def __init__(self):
        super().__init__()
        
        set_appearance_mode(APPEARANCE_MODE)
        set_default_color_theme(COLOUR_THEME)

        self.geometry(APP_GEOMETRY)
        self.title(APP_NAME)
        
        self.tabview = TabView(master=self)
        self.search_gui = Tab(master=self.tabview.search_tab, title="Search for Tickets")
        self.delay_gui = Tab(master=self.tabview.delay_tab, title="Delay Tickets")
        
        self.search_gui.conversation.add("bot", "Hello! How can I help you today?")
        self.search_gui.conversation.add("usr", "You can't help me!")
        
