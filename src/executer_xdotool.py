from src.executer_base import BaseExecutor
import subprocess
from src import utilities, constants
from src.view.view_base import SettingsItem
from src.classes.settings import Settings

TRIGGER_DELAY = "xdotool_triggerDelay"
TRIGGER_DELAY_DEFAULT = 100
TRIGGER_DELAY_JITTER = "xdotool_triggerDelayJitter"
TRIGGER_DELAY_JITTER_DEFAULT = 30
KEY_DELAY = "xdotool_stratagemKeyDelay"
KEY_DELAY_DEFAULT = 30
KEY_DELAY_JITTER = "xdotool_stratagemKeyDelayJitter"
KEY_DELAY_JITTER_DEFAULT = 20

class XdotoolExecuter(BaseExecutor):
    def __init__(self):
        super().__init__()
        self.settings = Settings.getInstance()
        self.isExecuting = False
        self.triggerKey = self.parse_macro_key(self.settings.triggerKey)
    
    def on_macro_triggered(self, macro):
        if self.isExecuting:
            return
        if macro is not None:
            self.isExecuting = True
            subprocess.call(["xdotool", "keydown", self.triggerKey])
        utilities.sleepMs(self.triggerDelay, self.triggerDelayJitter)
        for input in macro.commandArray:
            subprocess.call(["xdotool", "keydown", input])
            utilities.sleepMs(self.keyDelay, self.keyDelayJitter)
            subprocess.call(["xdotool", "keyup", input])
            utilities.sleepMs(self.keyDelay, self.keyDelayJitter)
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
        settings.append(SettingsItem("xdotool settings", None, None, constants.SETTINGS_VALUE_TYPE_HEADER))
        settings.append(SettingsItem("Trigger delay",TRIGGER_DELAY_DEFAULT, TRIGGER_DELAY, constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Trigger delay jitter", TRIGGER_DELAY_JITTER_DEFAULT, TRIGGER_DELAY_JITTER, constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Stratagem key delay", KEY_DELAY_DEFAULT, KEY_DELAY, constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Stratagem key delay jitter", KEY_DELAY_JITTER_DEFAULT, KEY_DELAY_JITTER, constants.SETTINGS_VALUE_TYPE_INT))

        return settings
    
    def prepare(self):
        self.triggerDelay = getattr(self.settings, TRIGGER_DELAY, TRIGGER_DELAY_DEFAULT)
        self.triggerDelayJitter = getattr(self.settings, TRIGGER_DELAY_JITTER, TRIGGER_DELAY_JITTER_DEFAULT)
        self.keyDelay = getattr(self.settings, KEY_DELAY, KEY_DELAY_DEFAULT)
        self.keyDelayJitter = getattr(self.settings, KEY_DELAY_JITTER, KEY_DELAY_JITTER_DEFAULT)