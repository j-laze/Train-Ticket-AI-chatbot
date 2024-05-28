import customtkinter as ctk
from tkinter import Listbox
from gui_utils import *



ctk.set_appearance_mode(APPEARANCE_MODE)
ctk.set_default_color_theme(COLOUR_THEME)

app = ctk.CTk()
app.geometry(APP_GEOMETRY)
app.title(APP_NAME)


tabview = TabView(master=app)

app.mainloop()
