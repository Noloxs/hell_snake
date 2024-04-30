import sys
from listener_pynput import PynputKeyListener
from model import Model
    
class Controller:
    def __init__(self, model):
        self.model = model
        if model.settings.selectedExecutor == "pynput":
            from executer_pynput import PynputExecuter
            self.executer = PynputExecuter(self.model)
        elif model.settings.selectedExecutor == "arduino":
            from executer_arduino import ArduinoPassthroughExecuter
            self.executer = ArduinoPassthroughExecuter(self.model)
        elif model.settings.selectedExecutor == "pyautogui":
            from executer_pyautogui import PyAutoGuiExecuter
            self.executer = PyAutoGuiExecuter(self.model)
        else:
            raise ModuleNotFoundError

        self.keyListener = PynputKeyListener(self.model, self)
    
    def set_view(self, view):
        self.view = view
        self.view.add_executor_settings(self.executer)
        #TODO Replace with last used loadout
        self.set_active_loadout(next(iter(self.model.settings.loadouts.keys())))

    def toggle_armed(self):
        self.set_armed(not self.model.isArmed)
    
    def set_armed(self, isArmed):
        self.model.set_armed(isArmed)
        self.view.update_armed()
    
    def show_change_macro_dialog(self, key):
        self.view.show_change_macro_dialog(key)

    def change_macro_binding(self, key, strategemId):
        strategem = self.model.strategems[strategemId]
        strategem.prepare_strategem(self.model, self.executer)
        self.model.change_macro_binding(key, strategemId)
        self.view.update_macros()
    
    def set_active_loadout(self, loadoutId):
        self.model.set_active_loadout(loadoutId)
        for key, strategem in self.model.macros.items():
            strategem.prepare_strategem(self.model, self.executer)
        self.view.update_current_loadout()
    
    def trigger_macro(self, strategem):
        self.executer.on_macro_triggered(strategem)
    
    def dump_settings(self):
        import json
        dump = json.dumps(self.model.settings, default=vars, indent=2)
        print(dump)
    
    def exit(self):
        sys.exit(0)