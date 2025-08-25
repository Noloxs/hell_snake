import constants
import sys
from src.model import Model
from src.executor.exceptions import ExecutorErrorException
from PyQt5.QtWidgets import QMessageBox

# The rest of your SerialBaseExecutor code...
class Controller:
    def __init__(self, model: Model):
        self._model = model
        self.loadouts_updated = False

        self._model.loadoutsManager.attach_change_listener(self.on_loadout_saved)

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
        elif selectedExecutor == constants.EXECUTOR_PICO:
            from src.executor.executer_pico import PicoPassthroughExecuter
            self.executer = PicoPassthroughExecuter(self)
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
        try:
            self.set_executor()
        except ExecutorErrorException as e:
            self.display_executor_error(e)
            self.on_exit()
        else:
            self.set_active_loadout(self._model.settingsManager.currentLoadoutId)
            self.view.show_interface()

    # ... and a keylistener callbacks
    def set_keylistener(self, keylistener):
        self.keylistener = keylistener

    def display_executor_error(self, error):
        error_message = f"Failed to set executor: {str(error)}"
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error_message)
        msg.setWindowTitle("Executor Error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

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

    def get_active_loadout_id(self):
        return self._model.settingsManager.currentLoadoutId
    
    # Macros
    def getMacroForKey(self, key):
        return self._model.get_current_loadout_macros().get(key, None)
    
    def getAllMacros(self):
        return self._model.get_current_loadout_macros().items()

    # This is where 99% of the magic happens
    def trigger_macro(self, stratagem):
        try:
            self.executer.on_macro_triggered(stratagem)
        except ExecutorErrorException as e:
            print("Error sending to serial port: " + str(e))
            # TODO: Add UI error dialog here.

    # Hook to detect loadouts being saved
    def on_loadout_saved(self, event):
        if event['type'] == 'save':
            self.loadouts_updated = False
        elif event['type'] == 'import':
            self.loadouts_updated = True
            self.view.on_loadout_changed()

    # New methods for import/export
    def export_all_loadouts(self, filePath):
        """Export all loadouts to file."""
        self._model.export_all_loadouts(filePath)

    def import_all_loadouts(self, filePath):
        """Import all loadouts from file."""
        return self._model.import_all_loadouts(filePath)

    # Exit hook
    def on_exit(self):
        if self.loadouts_updated:
            if self.view.confirm_save_loadouts():
                self._model.loadoutsManager.saveToFile()
        self._model.settingsManager.saveToFile()
        sys.exit(0)