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
        self.view.show_interface()

    def toggle_armed(self):
        self.set_armed(not self.model.isArmed)
    
    def set_armed(self, isArmed):
        self.model.set_armed(isArmed)
        self.view.update_armed()
    
    def show_change_macro_dialog(self, key):
        self.view.show_change_macro_dialog(key)

    def update_macro_binding(self, key, strategemId):
        strategem = self.model.strategems[strategemId]
        strategem.prepare_strategem(self.model, self.executer)
        self.model.update_macro_binding(key, strategemId)
        self.view.update_macros()
    
    def add_loadout(self, loadoutName):
        self.model.add_loadout(loadoutName)
        self.view.on_loadout_changed()

    def update_loadout(self, id, loadout):
        self.model.update_loadout(id,loadout)
        if self.model.currentLoadoutId == id:
            self.set_active_loadout(id)
        self.view.on_loadout_changed()
    
    def set_active_loadout(self, loadoutId):
        self.model.set_active_loadout(loadoutId)
        for key, strategem in self.model.macros.items():
            strategem.prepare_strategem(self.model, self.executer)
        self.view.update_current_loadout()
    
    def trigger_macro(self, strategem):
        self.executer.on_macro_triggered(strategem)

    def save_settings(self):
        import json
        settings = json.dumps(self.model.settings, default=vars, indent=2)
        with open("settings.json", "w") as file:
            file.write(settings)
    
    def print_settings(self):
        import json
        settings = json.dumps(self.model.settings, default=vars, indent=2)
        print(settings)
    
    def exit(self):
        sys.exit(0)