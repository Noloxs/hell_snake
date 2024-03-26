import sys
import threading
from views import Overview, SettingsView
from config import macroKeys
from strategem import strategems
import macro_executer

class Model:
    def __init__(self):
        self.settings = {"theme": "light"}
        self.armed = False
        self.macros = {
                        "1": strategems[1],
                        "2": strategems[2],
                        "3": strategems[8],
                        "4": strategems[5],
                        "5": strategems[6],
                        "6": strategems[7],
                        "7": strategems[9],
                        "8": strategems[4],
                        "9": strategems[0]
                        }

    def get_setting(self, setting):
        return self.settings.get(setting)

    def set_setting(self, setting, value):
        self.settings[setting] = value

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def open_settings_window(self):
        settings_view = SettingsView(self)
        settings_view.mainloop()

    def change_theme(self, theme):
        self.model.set_setting("theme", theme)
        self.view.update_label(f"Theme changed to {theme}")
    
    def save_macros(self, macros):
        self.model.macros = macros
        self.view.update_macros()

    def toggle_armed(self):
        self.model.armed = not self.model.armed
        self.view.update_armed()
        macro_executer.arm(self.model.armed)
    
    def exit(self):
        sys.exit(0)

if __name__ == "__main__":
    model = Model()
    controller = Controller(model, None)
    overview = Overview(controller)
    controller.view = overview
    overview.mainloop()
