import customtkinter as ctk
from tkinter import Listbox
from gui_utils import *



ctk.set_appearance_mode(APPEARANCE_MODE)
ctk.set_default_color_theme(COLOUR_THEME)

app = ctk.CTk()
app.geometry(APP_GEOMETRY)
app.title(APP_NAME)

tabview = ctk.CTkTabview(master=app)
tabview.pack(pady=PADY)


search_tab = tabview.add(TAB_NAMES[0])
delay_tab = tabview.add(TAB_NAMES[1])


search_frame = ctk.CTkFrame(master=search_tab)
search_frame.pack(fill=FRAME_FILL, expand=FRAME_EXPAND, padx=FRAME_PADX, pady=FRAME_PADY)

search_title = ctk.CTkLabel(master=search_frame, text="Search for Tickets", font=TITLE_FONT)
search_title.pack(padx=PADX, pady=PADY)

search_prompt_listbox = Listbox(master=search_frame, selectmode=None, width=50, height=10)
search_prompt_listbox.pack(padx=PADX, pady=PADY)
search_prompt_listbox.bind("<Button-1>", lambda event: "break")
search_prompt_listbox.bind("<Key>", lambda event: "break")

search_prompt_entry = ctk.CTkEntry(master=search_frame, placeholder_text="Search Prompt")
search_prompt_entry.pack(padx=PADX, pady=PADY)

delay_frame = ctk.CTkFrame(master=delay_tab)
delay_frame.pack(fill=FRAME_FILL, expand=FRAME_EXPAND, padx=FRAME_PADX, pady=FRAME_PADY)

delay_title = ctk.CTkLabel(master=delay_frame, text="Delay Tickets", font=TITLE_FONT)
delay_title.pack(padx=PADX, pady=PADY)

delay_prompt_listbox = Listbox(master=delay_frame, selectmode=None, width=50, height=10)
delay_prompt_listbox.pack(padx=PADX, pady=PADY)
delay_prompt_listbox.bind("<Button-1>", lambda event: "break")
delay_prompt_listbox.bind("<Key>", lambda event: "break")

delay_prompt_entry = ctk.CTkEntry(master=delay_frame, placeholder_text="Delay Prompt")
delay_prompt_entry.pack(padx=PADX, pady=PADY)



search_prompt_listbox.insert("end", "")
for prompt, data in TEST_PROMPT_DATA:
    append_converse(prompt, data, search_prompt_listbox)



app.mainloop()
