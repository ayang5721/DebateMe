import tkinter as tk
from tkinter import filedialog
import os, json

from sympy import root

# ---------- Scrollable bubble list (Canvas + inner Frame) ----------
class ScrollableMessages(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.inner = tk.Frame(self.canvas)
        self.win = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        self.inner.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.vsb.pack(side="right", fill="y")



    def _on_frame_configure(self, _e=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, e):
        # keep inner frame same width as canvas
        self.canvas.itemconfig(self.win, width=e.width)

    def scroll_to_bottom(self):
        self.canvas.yview_moveto(1.0)
        # run again after geometry settles
        self.after(10, lambda: self.canvas.yview_moveto(1.0))

# ---------- Your screen ----------
def start_debate(take, current_user, root, on_back):
    # Make these “module-level” globals if you like, but cleaner is to close over them
    debate_path = f"{take['key']}_debate.jsonl"  # use JSONL for safe appends

    for widget in root.winfo_children():
        widget.destroy()

    top = tk.Frame(root)
    top.pack(fill="x", padx=8, pady=(8, 4))

    def _back():
        print("Exit clicked")  # debug
        try:
            # schedule back on the event loop; ensures start_debate returns first
            root.after(0, on_back)
        except Exception as e:
            import traceback; traceback.print_exc()

    tk.Button(top, text="← Exit", command=_back).grid(row=0, column=0, sticky="w")

    tk.Label(top, text=f"Debate {take['description']}", font=("Arial", 16)).grid(row=0, column=1)
    top.grid_columnconfigure(0, weight=1)
    top.grid_columnconfigure(1, weight=0)
    top.grid_columnconfigure(2, weight=1)



    # Scrollable bubble list
    messages_view = ScrollableMessages(root)
    messages_view.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    # Bottom input row
    bottom = tk.Frame(root)
    bottom.pack(fill="x", padx=8, pady=(0, 8))

    entry = tk.Entry(bottom)
    entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
    send_btn = tk.Button(bottom, text="Send")
    send_btn.pack(side="right")

    # Load history (JSONL)
    if os.path.exists(debate_path) and os.path.getsize(debate_path) > 0:
        with open(debate_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                is_me = (rec.get("user") == current_user.username)
                add_message(messages_view.inner, rec.get("message", ""), is_me=is_me)
    messages_view.scroll_to_bottom()
    entry.focus_set()

    # Send handlers
    def do_send(_evt=None):
        text = entry.get().strip()
        if not text:
            return
        entry.delete(0, tk.END)

        # append to UI
        add_message(messages_view.inner, text, is_me=True)
        messages_view.scroll_to_bottom()

        # persist as JSONL (one object per line)
        with open(debate_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"user": current_user.username, "message": text}, ensure_ascii=False))
            f.write("\n")

    send_btn.config(command=do_send)
    entry.bind("<Return>", do_send)

def add_message(parent, text, is_me=False, wrap=520-100):
    """Create a left/right-aligned bubble row inside `parent` (a Frame)."""
    row = tk.Frame(parent, padx=8, pady=4)
    row.pack(fill="x", expand=True)

    spacer = tk.Frame(row)
    bubble = tk.Frame(row, bg=("#DCF8C6" if is_me else "#FFFFFF"), bd=0, highlightthickness=0)
    bubble.configure(highlightbackground="#dddddd", highlightcolor="#dddddd", highlightthickness=1)

    lbl = tk.Label(
        bubble, text=text, bg=bubble["bg"],
        justify="left", wraplength=wrap, padx=10, pady=8
    )
    lbl.pack()

    if is_me:
        spacer.pack(side="left", fill="x", expand=True)
        bubble.pack(side="right", padx=6, pady=2)
    else:
        bubble.pack(side="left", padx=6, pady=2)
        spacer.pack(side="right", fill="x", expand=True)
