import tkinter as tk
import os, json
from classes import User, Take
import numpy as np
from tkinter import scrolledtext


def start_debate(take, current_user, root):

    global shared_take
    shared_take = take

    global shared_current_user
    shared_current_user = current_user 

    global shared_root
    shared_root = root

    for widget in root.winfo_children():
        widget.destroy()

    if os.path.exists(f"{take['key']}_debate.json") and os.path.getsize(f"{take['key']}_debate.json") > 0:
        with open(f"{take['key']}_debate.json", "r") as f:
            debate_data = json.load(f)
    else:
        debate_data = {}

    
    tk.Label(root, text=f"Debate {take['description']}", font=("Arial", 16)).pack(pady=10)
    debate_box = scrolledtext.ScrolledText(root, width=70, height=15, state='disabled')
    debate_box.pack(pady=10)

    entry = tk.Entry(root, width=40)
    entry.pack(side="left", fill="x", expand=True, padx=(8, 4), pady=8)

    for text in debate_data:
        if text['user'] == current_user.username:
            add_message(debate_box, text['message'], is_me=True)
        else:
            add_message(debate_box, text['message'], is_me=False)

    # --- send button ---
    send_btn = tk.Button(root, text="Send", command=lambda: add_message(debate_box, entry.get().strip(), is_me=True, new_message=True))
    send_btn.pack(side="right", padx=(0, 8), pady=8)

    # --- bind Enter key to same function ---
    entry.bind("<Return>", lambda event: add_message(debate_box, entry.get().strip(), is_me=True, new_message=True))






def add_message(ui_parent, text, is_me=False, wrap=420, new_message = False):
    """
    Create a row with a left/right-aligned bubble.
    """
    row = tk.Frame(ui_parent, padx=8, pady=4)
    row.pack(fill="x", expand=True)

    if new_message:
        with open(f"{shared_take['key']}_debate.json", "a") as f:
            json.dump(
                {
                "user": shared_current_user.username,
                    "message": text
                },
                f
            )
            f.write("\n")

        shared_root.yview_moveto(1.0)   # scroll to bottom


    # Spacer + bubble pattern to force alignment without grids
    spacer = tk.Frame(row)
    bubble = tk.Frame(row, bg=("#DCF8C6" if is_me else "#FFFFFF"), bd=0, highlightthickness=0)
    label = tk.Label(
        bubble,
        text=text,
        bg=bubble["bg"],
        justify="left",
        wraplength=wrap,
        padx=10,
        pady=8
    )

    # Rounded corners illusion (soften edges)
    bubble.configure(highlightbackground="#dddddd", highlightcolor="#dddddd", highlightthickness=1)

    label.pack()

    if is_me:
        # right-aligned: spacer eats left space
        spacer.pack(side="left", fill="x", expand=True)
        bubble.pack(side="right", padx=6, pady=2)
    else:
        # left-aligned: spacer eats right space
        bubble.pack(side="left", padx=6, pady=2)
        spacer.pack(side="right", fill="x", expand=True)





