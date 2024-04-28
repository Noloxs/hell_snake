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
        self.set_armed(not self.model.isArmed)
    
    def set_armed(self, isArmed):
        self.model.set_armed(isArmed)
        if(isArmed):
            for key, strategem in self.model.macros.items():
                strategem.prepare_strategem(self.model, self.executer)
        self.view.update_armed()
    
    def show_change_macro_dialog(self, key):
        dialog = FilterDialog(self, key)
        dialog.mainloop()

    def change_macro_binding(self, key, strategemId):
        strategem = self.model.strategems[strategemId]
        strategem.prepare_strategem(self.model, self.executer)
        self.model.change_macro_binding(key, strategem)
        self.view.update_macros()
    
    def change_active_loadout(self, loadoutId):
        self.model.set_active_loadout(loadoutId)
        self.view.update_current_loadout()
        self.view.update_macros()
    
    def trigger_macro(self, strategem):
        self.executer.on_macro_triggered(strategem)
    
    def dump_settings(self):
        import json
        dump = json.dumps(self.model.settings, default=vars, indent=2)
        print(dump)
    
    def exit(self):
        sys.exit(0)