import tkinter as tk

def validate_entry(char):
    return char == "" or (char.isdigit() and len(char) <= 7)


# Create the main window
root = tk.Tk()
root.title("Entry Limit Example")



# Create an Entry widget with validation
entry = tk.Entry(root, validate="key", validatecommand=(root.register(validate_entry), '%P'))
entry.pack(padx=20, pady=20)

# Start the Tkinter event loop
root.mainloop()