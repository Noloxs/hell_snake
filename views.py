
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import simpledialog
from executer_arduino import ArduinoPassthroughExecuter

class Overview(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Hell Snake")

        self.minsize("350", "350")

        ico = Image.open('icons/hell_snake.png')
        photo = ImageTk.PhotoImage(ico)
        self.wm_iconphoto(False, photo)

        self.loadoutLabel = tk.Label(self, font=("Arial", 24, "bold") )
        self.loadoutLabel.pack(side="top", fill="x")
        self.update_current_loadout()

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
        self.settings_menu.add_command(label="Dump settings", command=self.controller.dump_settings)
        self.settings_menu.add_command(label="Exit", command=self.controller.exit)

        self.menu.add_command(label="Arm", command=controller.toggle_armed)

        self.loadout_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Loadputs", menu=self.loadout_menu)
        self.update_choose_loadouts()

        self.update_armed()

    def update_macros(self):
        for widget in self.macros_frame.winfo_children():
            widget.destroy()

        for index, (key, value) in enumerate(self.controller.model.macros.items()):
            # Add item frame
            self.macro_frame = tk.Frame(self.macros_frame)
            self.macro_frame.pack(side="top", anchor="nw", pady=5, padx=5, fill="x")

            # Add icon
            image = Image.open("icons/"+value.icon_name+".webp")
            image = image.resize((50, 50), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            icon_label = tk.Label(self.macro_frame, image=photo)
            icon_label.image = photo
            icon_label.grid(row=index, column=0, padx=10)
            icon_label.bind("<Button-1>", lambda event, key=key: self.controller.show_change_macro_dialog(key))

            # Add key
            key_label = tk.Label(self.macro_frame, text=key, font=("Arial", 24, "bold"))
            key_label.grid(row=index, column=1, padx=10)
            key_label.bind("<Button-1>", lambda event, key=key: self.controller.show_change_macro_dialog(key))

            # Add name
            name_label = tk.Label(self.macro_frame, text=value.name)
            name_label.grid(row=index, column=2, columnspan=3, padx=10, sticky="w")
            name_label.bind("<Button-1>", lambda event, key=key: self.controller.show_change_macro_dialog(key))

            self.macro_frame.bind("<Button-1>", lambda event, key=key: self.controller.show_change_macro_dialog(key))
    
    def update_armed(self):
        if self.controller.model.armed:
            self.label.config(text="ARMED", background="red")
            self.menu.entryconfig(2, label="Disarm")
        else:
            self.label.config(text="DISARMED", background="green")
            self.menu.entryconfig(2, label="Arm")
    
    def update_choose_loadouts(self):
        for loadoutId, loadout in self.controller.model.settings.loadouts.items():
            self.loadout_menu.add_command(label=loadout.name, command=lambda loadoutId=loadoutId: self.controller.change_active_loadout(loadoutId))
    
    def update_current_loadout(self):
        currentLoadout = self.controller.model.currentLoadout
        self.loadoutLabel.config(text="Loadout: "+currentLoadout.name)

    def add_executor_settings(self, executor):
        if isinstance(executor,ArduinoPassthroughExecuter):
            self.serial_menu = tk.Menu(self.menu, tearoff=0)
            self.menu.add_cascade(label="Select serial", menu=self.serial_menu)
            
            physical_addresses = executor.get_physical_addresses()
            for port, desc, hwid in sorted(physical_addresses):
                self.serial_menu.add_command(label=desc, command=lambda port=port: executor.connect_to_arduino(port))

class SettingsView(tk.Toplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Settings")

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

class Item:
    def __init__(self, icon, name, description):
        self.icon = icon
        self.name = name
        self.description = description

class FilterDialog(tk.Toplevel):
    def __init__(self, controller, key):
        super().__init__()
        self.title("Filter Dialog")

        self.key = key

        self.controller = controller
    
        self.filter_var = tk.StringVar()
        self.filter_var.trace("w", self.filter_items)

        self.create_widgets()

    def create_widgets(self):
        # Input field
        self.input_label = tk.Label(self, text="Search:")
        self.input_label.grid(row=0, column=0, padx=5, pady=5)
        self.input_entry = tk.Entry(self, textvariable=self.filter_var)
        self.input_entry.grid(row=0, column=1, padx=5, pady=5)

        self.macros_frame = tk.Frame(self)
        self.macros_frame.grid(row=1, column=0, columnspan=2, pady=5, padx=5)

        self.update_macros("")

        self.input_entry.focus_set()

    def on_item_click(self, key, id):
        self.controller.change_macro_binding(key, id)
        self.destroy()

    def update_macros(self, filter):
        for widget in self.macros_frame.winfo_children():
            widget.destroy()

        i = 0
        for id, strategem in self.controller.model.strategems.items():
            if filter in strategem.name.lower():
                # Add item frame
                self.macro_frame = tk.Frame(self.macros_frame)
                self.macro_frame.pack(side="top", anchor="nw", pady=1, fill="x")

                # Add icon
                image = Image.open("icons/"+strategem.icon_name+".webp")
                image = image.resize((25, 25), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                icon_label = tk.Label(self.macro_frame, image=photo)
                icon_label.image = photo
                icon_label.grid(row=i, column=0, padx=5)
                icon_label.bind("<Button-1>", lambda event, id=id: self.on_item_click(self.key, id))

                # Add name
                name_label = tk.Label(self.macro_frame, text=strategem.name)
                name_label.grid(row=i, column=1, columnspan=3, sticky="w")
                name_label.bind("<Button-1>", lambda event, id=id: self.on_item_click(self.key, id))

                self.macro_frame.bind("<Button-1>", lambda event, id=id: self.on_item_click(self.key, id))

                i = i+1

    def filter_items(self, *args):
        # Get the text entered in the input field
        filter_text = self.filter_var.get().lower()

        self.update_macros(filter_text)