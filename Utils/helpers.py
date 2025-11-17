import tkinter as tk

# Ghost text for username and password fields
def add_placeholder(entry: tk.Entry, placeholder: str, color: str = "grey") -> None:
    def on_focus_in(event) -> None:
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def on_focus_out(event) -> None:
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg=color)

    entry.insert(0, placeholder)
    entry.config(fg=color)
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)