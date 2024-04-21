import sys
from views import Overview, SettingsView,FilterDialog
from executer_pynput import PynputExecuter
from executer_arduino import ArduinoPassthroughExecuter
from executer_pyautogui import PyAutoGuiExecuter
from listener_pynput import PynputKeyListener
from model import Model
    
class Controller:
    def __init__(self, model):
        self.model = model
        if model.settings.selectedExecutor == "pynput":
            self.executer = PynputExecuter(self.model)
        elif model.settings.selectedExecutor == "arduino":
            self.executer = ArduinoPassthroughExecuter(self.model)
        elif model.settings.selectedExecutor == "pyautogui":
            self.executer = PyAutoGuiExecuter(self.model)
        else:
            raise ModuleNotFoundError

        self.keyListener = PynputKeyListener(self.model, self)
    
    def set_view(self, view):
        self.view = view
        self.view.add_executor_settings(self.executer)

    def open_settings_window(self):
        settings_view = SettingsView(self)
        settings_view.mainloop()
    
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