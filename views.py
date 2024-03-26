
import tkinter as tk
from PIL import ImageTk, Image

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

        self.macros_frame = tk.Frame(self)
        self.macros_frame.pack(pady=10)

        # Add sample values to the hashmap
        sample_macros = {
            "Macro1": Macro("path/to/icon1.png", "Macro 1 Name"),
            "Macro2": Macro("path/to/icon2.png", "Macro 2 Name"),
            "Macro3": Macro("path/to/icon3.png", "Macro 3 Name")
        }

        for key, value in sample_macros.items():
            self.add_macro_row(key, value)

        self.add_button = tk.Button(self, text="Add Macro", command=self.add_macro_row)
        self.add_button.pack(pady=5)

        self.save_button = tk.Button(self, text="Save", command=self.save_macros)
        self.save_button.pack(pady=5)

    def add_macro_row(self, key=None, value=None):
        row = len(self.macros_frame.winfo_children()) // 2

        key_entry = tk.Entry(self.macros_frame)
        key_entry.grid(row=row, column=0)
        key_entry.insert(0, key if key else "")

        name_entry = tk.Entry(self.macros_frame)
        name_entry.grid(row=row, column=1)
        name_entry.insert(0, value.name if value else "")

        remove_button = tk.Button(self.macros_frame, text="Remove", command=lambda: self.remove_macro_row(row))
        remove_button.grid(row=row, column=2)

    def remove_macro_row(self, row):
        for widget in self.macros_frame.grid_slaves(row=row):
            widget.grid_forget()

    def save_macros(self):
        macros = {}
        for i in range(len(self.macros_frame.winfo_children()) // 2):
            key = self.macros_frame.grid_slaves(row=i, column=0)[0].get()
            name = self.macros_frame.grid_slaves(row=i, column=1)[0].get()
            if key and name:
                macros[key] = Macro("sample_icon_path", name)  # Sample icon path used for demonstration

        self.controller.save_macros(macros)