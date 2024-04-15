import sys
from views import Overview, SettingsView,FilterDialog
from executer_pynput import PynputExecuter
from executer_arduino import ArduinoPassthroughExecuter
from listener_pynput import PynputKeyListener
from model import Model
    
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        #self.executer = PynputExecuter(self.model)
        self.executer = ArduinoPassthroughExecuter(self.model)
        self.executer.connect_to_arduino("port")
        self.keyListener = PynputKeyListener(self.model, self)

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
        for key, strategem in self.model.macros.items():
            strategem.prepare_strategem()
        self.view.update_armed()
        self.keyListener.arm(self.model.armed)
    
    def show_change_macro_dialog(self, key):
        dialog = FilterDialog(self, key)
        dialog.mainloop()

    def change_macro_binding(self, key, strategemId):
        self.model.change_macro_binding(key, strategemId)
        self.view.update_macros()
    
    def change_active_loadout(self, loadoutId):
        self.model.set_active_loadout(loadoutId)
        self.view.update_current_loadout()
        self.view.update_macros()
    
    def trigger_macro(self, strategem):
        self.executer.on_macro_triggered(strategem)
    
    def exit(self):
        sys.exit(0)