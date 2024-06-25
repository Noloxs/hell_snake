import constants
import sys
from src.model import Model
from src.settings import Settings
from src.listener_pynput import PynputKeyListener
    
class Controller:
    def __init__(self, model: Model):
        self.model = model
        self.settings = Settings.getInstance()

        self.loadouts_updated = False

        self.keyListener = PynputKeyListener(self.model, self)

    def set_executor(self):
        if hasattr(self, "executer"):
            self.executer.stop()

        selectedExecutor = self.settings.selectedExecutor
        if selectedExecutor == constants.EXECUTOR_PYNPUT:
            from src.executer_pynput import PynputExecuter
            self.executer = PynputExecuter()
        elif selectedExecutor == constants.EXECUTOR_ARDUINO:
            from src.executer_arduino import ArduinoPassthroughExecuter
            self.executer = ArduinoPassthroughExecuter(self)
        elif selectedExecutor == constants.EXECUTOR_PYAUTOGUI:
            from src.executer_pyautogui import PyAutoGuiExecuter
            self.executer = PyAutoGuiExecuter()
        elif selectedExecutor == constants.EXECUTOR_XDOTOOL:
            from src.executer_xdotool import XdotoolExecuter
            self.executer = XdotoolExecuter()
        else:
            raise ModuleNotFoundError
        self.view.update_executor_menu()
        self.executer.start()

    def update_executor_menu(self):
        self.view.update_executor_menu()
    
    def on_settings_changed(self):
        self.view.on_settings_changed()

    def set_view(self, view):
        self.view = view
        self.set_executor()
        if hasattr(self.settings, "currentLoadoutId"):
            self.set_active_loadout(self.settings.currentLoadoutId)
        self.view.show_interface()

    def toggle_armed(self):
        self.set_armed(not self.model.isArmed)
    
    def set_armed(self, isArmed):
        self.model.set_armed(isArmed)
        if isArmed:
            self.executer.prepare()
        self.view.update_armed()

    def cycle_loadout(self, offset):
        # Get current active loadout ID and available loadout IDs
        current_loadout_id = self.model.currentLoadoutId
        loadout_ids = list(self.model.loadoutManager.loadouts.keys())
        
        # Calculate the index of the next loadout
        current_index = loadout_ids.index(current_loadout_id)
        new_index = (current_index + offset + len(loadout_ids)) % len(loadout_ids)
        
        # Set the next loadout as active
        self.set_active_loadout(loadout_ids[new_index])

    def update_title_description(self, description):
        self.view.update_title_description(description)

    def show_change_macro_dialog(self, key):
        self.view.show_change_macro_dialog(key)

    def update_macro_binding(self, key, stratagemId):
        stratagem = self.model.stratagems[stratagemId]
        stratagem.prepare_stratagem(self.executer)
        self.model.update_macro_binding(key, stratagemId)
        self.loadouts_updated = True
        self.view.update_macros()

    def add_loadout(self, loadoutName):
        self.model.loadoutManager.addLoadout(loadoutName)
        self.set_active_loadout(self.model.loadoutManager.getCurrentLoadout())
        self.loadouts_updated = True
        self.view.update_loadout_menu_items()
    
    def delete_loadout(self, loadoutId):
        self.model.loadoutManager.deleteLoadout(loadoutId)
        self.set_active_loadout(self.model.loadoutManager.getCurrentLoadout())
        self.loadouts_updated = True
        self.view.update_loadout_menu_items()

    def update_loadout(self, id, loadout):
        self.model.loadoutManager.updateLoadout(id, loadout)
        self.set_active_loadout(id)
        self.loadouts_updated = True
        self.view.update_loadout_menu_items()
    
    def set_active_loadout(self, loadoutId):
        self.model.set_active_loadout(loadoutId)
        for key, stratagem in self.model.macros.items():
            stratagem.prepare_stratagem(self.executer)
        self.settings.currentLoadoutId = loadoutId
        self.view.update_current_loadout()
    
    def trigger_macro(self, stratagem):
        self.executer.on_macro_triggered(stratagem)
    
    def on_exit(self):
        if self.loadouts_updated:
            if self.view.confirm_save_loadouts():
                self.model.loadoutManager.saveToFile()
        self.settings.saveToFile()
        sys.exit(0)