
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import simpledialog

class Overview(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Simple GUI with Settings")
        self.geometry("400x300")

        self.label = tk.Label(self, font=("Arial", 24, "bold") )
        self.label.pack(side="top", fill="x")

        self.macros_frame = tk.Frame(self)
        self.macros_frame.pack(side="top", anchor="nw", pady=5, fill="x")

        self.update_macros()

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.settings_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.settings_menu)
        self.settings_menu.add_command(label="Settings", command=self.controller.open_settings_window)
        self.settings_menu.add_command(label="Exit", command=self.controller.exit)

        self.menu.add_command(label="Arm", command=controller.toggle_armed)

        self.update_armed()

    def update_macros(self):
        for widget in self.macros_frame.winfo_children():
            widget.destroy()

        self.geometry("400x610")

        for index, (key, value) in enumerate(self.controller.model.macros.items()):
            # Add icon
            image = Image.open("icons/"+value.icon_name+".webp")
            image = image.resize((50, 50), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            icon_label = tk.Label(self.macros_frame, image=photo)
            icon_label.image = photo
            icon_label.grid(row=index, column=0, padx=10, pady=5)

            # Add key
            key_label = tk.Label(self.macros_frame, text=key, font=("Arial", 24, "bold"))
            key_label.grid(row=index, column=1, padx=10)

            # Add name
            name_label = tk.Label(self.macros_frame, text=value.name)
            name_label.grid(row=index, column=2, columnspan=3, sticky="w")
    
    def update_armed(self):
        if self.controller.model.armed:
            self.label.config(text="ARMED", background="red")
            self.menu.entryconfig(2, label="Disarm")
        else:
            self.label.config(text="DISARMED", background="green")
            self.menu.entryconfig(2, label="Arm")

class SettingsView(tk.Toplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Settings")
        self.geometry("500x400")

        self.delay_label = tk.Label(self, text="Trigger delay")
        self.delay_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="w")

        # Validation command for decimal number input
        self.validate_decimal_command = (self.register(self.validate_decimal), '%P')

        # Max input field
        self.max_label = tk.Label(self, text="Max:")
        self.max_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.max_entry = tk.Entry(self, validate='key', validatecommand=self.validate_decimal_command)
        self.max_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="w")
        
        # Min input field
        self.min_label = tk.Label(self, text="Min:")
        self.min_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.min_entry = tk.Entry(self, validate='key', validatecommand=self.validate_decimal_command)
        self.min_entry.grid(row=2, column=1, columnspan=2,  padx=5, pady=5, sticky="w")
        
        # List of strings
        self.strings_label = tk.Label(self, text="List of macro keys:")
        self.strings_label.grid(row=0, column=4, columnspan=2, padx=5, pady=5, sticky="w")
        self.strings_listbox = tk.Listbox(self)
        self.strings_listbox.grid(row=1, column=4, columnspan=2, rowspan=5, padx=5, pady=5)
        self.add_string_button = tk.Button(self, text="Add", command=self.add_string)
        self.add_string_button.grid(row=6, column=4, padx=5, pady=5)
        self.remove_string_button = tk.Button(self, text="Remove", command=self.add_string)
        self.remove_string_button.grid(row=6, column=5, padx=5, pady=5)
        
        # Buttons for arrow keys and trigger
        self.strategem_keys_label = tk.Label(self, text="Strategem keys")
        self.strategem_keys_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="w")

        self.up_button = tk.Button(self, text="UP", command=lambda: self.save_key("UP"))
        self.up_button.grid(row=5, column=1, padx=5, pady=5)
        
        self.down_button = tk.Button(self, text="DOWN", command=lambda: self.save_key("DOWN"))
        self.down_button.grid(row=6, column=1, padx=5, pady=5)
        
        self.left_button = tk.Button(self, text="LEFT", command=lambda: self.save_key("LEFT"))
        self.left_button.grid(row=6, column=0, padx=5, pady=5)
        
        self.right_button = tk.Button(self, text="RIGHT", command=lambda: self.save_key("RIGHT"))
        self.right_button.grid(row=6, column=2, padx=5, pady=5)
        
        self.trigger_button = tk.Button(self, text="TRIGGER", command=lambda: self.save_key("TRIGGER"))
        self.trigger_button.grid(row=5, column=2, padx=5, pady=5)
        
    def add_string(self):
        string = simpledialog.askstring("Add String", "Enter a single character:")
        if string and len(string) == 1:
            self.strings_listbox.insert(tk.END, string)
    
    def save_key(self, key):
        self.last_pressed_label.config(text="Last Pressed: " + key)
    
    def validate_decimal(self, value):
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False