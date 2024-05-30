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


# class Content(CTkFrame):
#     def __init__(self, master: CTkBaseClass, title: str, **kwargs):
#         super().__init__(master=master, **kwargs)
#         
#         self.pack(fill=FRAME_FILL, expand=FRAME_EXPAND)
#         
#         self.title = CTkLabel(master=self, text=title, font=TITLE_FONT)
#         self.title.pack(pady=PADY, padx=PADX)
# 
#         self.conversation = Conversation(master=self)
#         
#         self.entry = CTkEntry(master=self, placeholder_text="...")
#         self.entry.bind("<Return>", self.send_msg)
#         self.entry.pack(padx=PADX, pady=PADY)
#         
#     def send_msg(self, event):
#         self.conversation.add("usr", self.entry.get())
#         self.entry.delete(0, "end")


# class App(CTk):
#     def __init__(self):
#         super().__init__()
#         
#         set_appearance_mode(APPEARANCE_MODE)
#         set_default_color_theme(COLOUR_THEME)
# 
#         self.geometry(APP_GEOMETRY)
#         self.title(APP_NAME)
# 
#         self.gui = Content(master=self, title="Search for Tickets")
#         
#         self.gui.conversation.add("bot", "Hello! How can I help you today?")
#         self.gui.conversation.add("usr", "You can't help me!")


class App(CTk):
    def __init__(self):
        super().__init__()
        
        self.messages: list[(str, str)] = []

        set_appearance_mode(APPEARANCE_MODE)
        set_default_color_theme(COLOUR_THEME)

        self.geometry(APP_GEOMETRY)
        self.title(APP_NAME)
        
        self.frame = CTkFrame(master=self)
        self.frame.pack(fill=FRAME_FILL, expand=FRAME_EXPAND)

        self.header = CTkLabel(master=self.frame, text="Search for Tickets", font=TITLE_FONT)
        self.header.pack(pady=PADY, padx=PADX)
        
        self.conversation = Conversation(master=self.frame)
        
        self.entry = CTkEntry(master=self.frame, placeholder_text="...")
        self.entry.bind("<Return>", self.send_usr_msg)
        self.entry.pack(padx=PADX, pady=PADY)
        
    def waiting_user_in(self):
        return self.messages[-1][0] == "bot"
    
    def waiting_bot_out(self):
        return not self.waiting_user_in()
        
    def send_usr_msg(self, _):
        if self.waiting_user_in:
            self.messages.append(("usr", self.entry.get()))
            self.conversation.add("usr", self.entry.get())
            self.entry.delete(0, "end")
            
    def send_bot_msg(self, msg):
        self.messages.append(("bot", msg))
        self.conversation.add("bot", msg)