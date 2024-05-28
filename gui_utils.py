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

TAB_NAMES = [ "Ticket Search", "Delay Info" ]

## FRAME:

FRAME_FILL = "both"
FRAME_EXPAND = True
FRAME_PADX = 4*PADX
FRAME_PADY = 4*PADX

## TITLES:

TITLE_FONT = ("Arial", 20)
TITLE_PADX = 10
TITLE_PADY = 20

## PROMPTS:

LISTBOX_WIDTH_CHARS  = 50
LISTBOX_HEIGHT_CHARS = 15

TEST_PROMPT_DATA = [
    ( "prompty_prompt_01", [ "data", "atad" ] ),
    ( "prompty_prompt_02", [ "data", "atad" ] ),
    ( "prompty_prompt_03", [ "data", "atad" ] ),
    ( "prompty_prompt_04", [ "data", "atad" ] ),
    ( "prompty_prompt_05", [ "data", "atad" ] ),
    ( "prompty_prompt_06", [ "data", "atad" ] ),
    ( "prompty_prompt_07", [ "data", "atad" ] ),
    ( "prompty_prompt_08", [ "data", "atad" ] ),
    ( "prompty_prompt_09", [ "data", "atad" ] ),
    ( "prompty_prompt_10", [ "data", "atad" ] ),
    ( "prompty_prompt_11", [ "data", "atad" ] ),
    ( "prompty_prompt_12", [ "data", "atad" ] ),
    ( "prompty_prompt_13", [ "data", "atad" ] ),
    ( "prompty_prompt_14", [ "data", "atad" ] ),
    ( "prompty_prompt_15", [ "data", "atad" ] ),
    ( "prompty_prompt_16", [ "data", "atad" ] ),
]

################################|###############################
############################FUNCTIONS###########################
################################|###############################

def append_converse(question, data, listbox):
    listbox.insert("end", question)
    dlen = len(data)
    if dlen > 0:
        derived_str = "  " + data[0]
        if dlen > 1:
            for d in data[1:]:
                derived_str += f", {d}"
        listbox.insert("end", derived_str)
    listbox.insert("end", "")

################################|###############################
#############################CLASSES############################
################################|###############################


class Tab(CTkFrame):

    def __init__(self, master, title, **kwargs):

        super().__init__(master=master, **kwargs)
        
        self.pack(fill=FRAME_FILL, expand=FRAME_EXPAND)
        
        self.title = CTkLabel(master=self, text=title, font=TITLE_FONT)
        self.title.pack(pady=PADY/2)
        
        self.conversation = Listbox(master=self, selectmode=None, width=LISTBOX_WIDTH_CHARS, height=LISTBOX_HEIGHT_CHARS)
        self.conversation.pack(padx=PADX, pady=PADY)
        self.conversation.bind("<Button-1>", lambda event: "break")
        self.conversation.bind("<Key>", lambda event: "break")
        
        self.entry = CTkEntry(master=self, placeholder_text="...")
        self.entry.pack(padx=PADX, pady=PADY)


class TabView(CTkTabview):

    def __init__(self, master, **kwargs):
        
        super().__init__(master=master, **kwargs)
        
        self.pack()
        
        self.search_tab = self.add(TAB_NAMES[0])
        self.delay_tab = self.add(TAB_NAMES[1])


class Gui(CTk):
    
    def __init__(self):

        set_appearance_mode(APPEARANCE_MODE)
        set_default_color_theme(COLOUR_THEME)
        
        super().__init__()

        self.geometry(APP_GEOMETRY)
        self.title(APP_NAME)
        
        self.tabview = TabView(master=self)
        self.search_gui = Tab(master=self.tabview.search_tab, title="Search for Tickets")
        self.delay_gui = Tab(master=self.tabview.delay_tab, title="Delay Tickets")
        