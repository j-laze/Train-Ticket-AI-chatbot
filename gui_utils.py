import customtkinter as ctk
from collections import namedtuple



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
