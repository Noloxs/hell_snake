from src.executer_base import BaseExecutor
import subprocess
from src import utilities, constants
from src.executer_base import SettingsItem

class XdotoolExecuter(BaseExecutor):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.isExecuting = False
        self.triggerKey = self.parse_macro_key(self.model.settings.triggerKey)
    
    def on_macro_triggered(self, macro):
        if self.isExecuting:
            print("Ignore, executing")
            return
        if macro is not None:
            self.isExecuting = True
            subprocess.call(["xdotool", "keydown", self.triggerKey])
        utilities.sleepTriggerKey(self.model)
        for input in macro.commandArray:
            subprocess.call(["xdotool", "keydown", input])
            utilities.sleepStratagemKey(self.model)
            subprocess.call(["xdotool", "keyup", input])
            utilities.sleepStratagemKey(self.model)
        subprocess.call(["xdotool", "keyup", self.triggerKey])
        self.isExecuting = False

    def parse_macro_key(self, key):
        if key in self.key_map:
            return self.key_map[key]
        else:
            return key

    key_map = {
        "shift":"Shift",
        "ctrl":"Ctrl",
        "up":"Up",
        "down":"Down",
        "left":"Left",
        "right":"Right",
        "caps_lock":"Caps_Lock"
        } 
    
    def get_settings_items(self):
        settings = []
        # TODO Update settings keys to be executor exclusive
        settings.append(SettingsItem("Trigger delay", "triggerDelay", constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Trigger delay jitter", "triggerDelayJitter", constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Stratagem key delay", "stratagemKeyDelay", constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Stratagem key delay jitter", "stratagemKeyDelayJitter", constants.SETTINGS_VALUE_TYPE_INT))

        return settings