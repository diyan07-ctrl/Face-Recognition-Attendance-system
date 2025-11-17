import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Radio Test")
        self.geometry("520x360")

        # Container to hold all pages
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        # Initialize pages
        for Page in (HomePage, DeletePage):
            name = Page.__name__
            frame = Page(container, self.show_frame)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[name] = frame

        self.show_frame("HomePage")

    def show_frame(self, name: str):
        """Raises the requested frame."""
        frame = self.frames[name]
        frame.tkraise()
        # If page has a reset() method, call it
        if hasattr(frame, "reset"):
            frame.reset()


# ---------------------------
# HOME PAGE
# ---------------------------

class HomePage(tk.Frame):
    def __init__(self, parent, show_frame):
        super().__init__(parent)
        tk.Label(self, text="Home Page", font=("Arial", 18)).pack(pady=40)
        tk.Button(self, text="Go to Delete Page",
                  command=lambda: show_frame("DeletePage")).pack()


# ---------------------------
# DELETE PAGE (Radio Buttons)
# ---------------------------

class DeletePage(tk.Frame):
    def __init__(self, parent, show_frame):
        super().__init__(parent)

        tk.Label(self, text="Delete Account Page", font=("Arial", 18)).pack(pady=20)

        # Shared variable — empty means no radio selected
        self.account_type = tk.StringVar(value="")

        # Frame for radio buttons
        radio_frame = tk.Frame(self)
        radio_frame.pack(pady=10)

        tk.Radiobutton(radio_frame, text="Professor",
                       value="prof", variable=self.account_type).pack(side="left", padx=20)

        tk.Radiobutton(radio_frame, text="TA",
                       value="TA", variable=self.account_type).pack(side="left", padx=20)

        tk.Button(self, text="Back to Home",
                  command=lambda: show_frame("HomePage")).pack(pady=20)

    def reset(self):
        """Reset radio buttons when page is shown."""
        self.account_type.set("")


# ---------------------------

if __name__ == "__main__":
    App().mainloop()
