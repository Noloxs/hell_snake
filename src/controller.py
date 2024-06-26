import constants
import sys
from src.model import Model
    
class Controller:
    def __init__(self, model: Model):
        self._model = model
        self.loadouts_updated = False

    # Allow view direct access to model components
    def get_settings_manager(self):
        return self._model.settingsManager

    def get_loadouts_manager(self):
        return self._model.loadoutsManager

    def get_stratagems(self):
        return self._model._stratagems

    # Executer initializiation
    def get_executor(self):
        return self.executer

    def set_executor(self):
        if hasattr(self, "executer"):
            self.executer.stop()

        selectedExecutor = self._model.settingsManager.selectedExecutor
        if selectedExecutor == constants.EXECUTOR_PYNPUT:
            from src.executor.executer_pynput import PynputExecuter
            self.executer = PynputExecuter(self)
        elif selectedExecutor == constants.EXECUTOR_ARDUINO:
            from src.executor.executer_arduino import ArduinoPassthroughExecuter
            self.executer = ArduinoPassthroughExecuter(self)
        elif selectedExecutor == constants.EXECUTOR_PYAUTOGUI:
            from src.executor.executer_pyautogui import PyAutoGuiExecuter
            self.executer = PyAutoGuiExecuter(self)
        elif selectedExecutor == constants.EXECUTOR_XDOTOOL:
            from src.executor.executer_xdotool import XdotoolExecuter
            self.executer = XdotoolExecuter(self)
        else:
            raise ModuleNotFoundError
        self.view.update_executor_menu()
        self.executer.start()
        self._model.prepare_stratagems(self)

    def update_executor_menu(self):
        self.view.update_executor_menu()
    
    def on_settings_changed(self):
        self.view.on_settings_changed()

    # Dependency injecting the view
    def set_view(self, view):
        self.view = view
        self.set_executor()
        self.set_active_loadout(self._model.settingsManager.currentLoadoutId)
        self.view.show_interface()

    # Arming and disarming
    def toggle_armed(self):
        self.set_armed(not self._model.is_armed)
    
    def set_armed(self, isArmed):
        self._model.set_armed(isArmed)
        if isArmed:
            self.executer.prepare()
        self.view.update_armed()
    
    def is_armed(self):
        return self._model.is_armed

    # Hotkey selection of loadouts
    def cycle_loadout(self, offset):
        # Get current active loadout ID and available loadout IDs
        current_loadout_id = self._model.settingsManager.currentLoadoutId
        loadout_ids = list(self._model.loadoutsManager.loadouts.keys())
        
        # Calculate the index of the next loadout
        current_index = loadout_ids.index(current_loadout_id)
        new_index = (current_index + offset + len(loadout_ids)) % len(loadout_ids)
        
        # Set the next loadout as active
        self.set_active_loadout(loadout_ids[new_index])

    # Presentation and interactions with macro selection
    def update_title_description(self, description):
        self.view.update_title_description(description)

    def show_change_macro_dialog(self, key):
        self.view.show_change_macro_dialog(key)

    def update_macro_binding(self, key, stratagemId):
        self._model.update_macro_binding(key, stratagemId)
        self.loadouts_updated = True
        self.view.update_macros()

    # Loadout list manipulation
    def add_loadout(self, loadoutName):
        loadoutId = self._model.loadoutsManager.addLoadout(loadoutName)
        self.set_active_loadout(loadoutId)
        self.loadouts_updated = True
        self.view.on_loadout_changed()
    
    def delete_loadout(self, loadoutId):
        self._model.loadoutsManager.deleteLoadout(loadoutId)
        self.set_active_loadout(next(iter(self._model.loadoutsManager.loadouts)))
        self.loadouts_updated = True
        self.view.on_loadout_changed()

    def update_loadout(self, id, loadout):
        self._model.loadoutsManager.updateLoadout(id, loadout)
        self.set_active_loadout(id)
        self.loadouts_updated = True
        self.view.on_loadout_changed()
    
    # Active loadout
    def set_active_loadout(self, loadoutId):
        if loadoutId in self._model.loadoutsManager.loadouts:
            self._model.settingsManager.currentLoadoutId = loadoutId
        self.view.update_current_loadout()
    
    def get_active_loadout(self):
        return self._model.loadoutsManager.loadouts.get(self._model.settingsManager.currentLoadoutId, None)
    
    # Macros
    def getMacroForKey(self, key):
        return self._model.get_current_loadout_macros().get(key, None)
    
    def getAllMacros(self):
        return self._model.get_current_loadout_macros().items()

    # This is where 99% of the magic happens
    def trigger_macro(self, stratagem):
        self.executer.on_macro_triggered(stratagem)
    
    # Exit hook
    def on_exit(self):
        if self.loadouts_updated:
            if self.view.confirm_save_loadouts():
                self._model.loadoutsManager.saveToFile()
        self._model.settingsManager.saveToFile()
        sys.exit(0)