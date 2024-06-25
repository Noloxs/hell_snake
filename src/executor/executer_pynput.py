import constants
import utilities
from pynput.keyboard import Controller
from src.executer_base import BaseExecutor
from src.key_parser_pynput import PynputKeyparser
from src.view.view_base import SettingsItem

TRIGGER_DELAY = "pynput_triggerDelay"
TRIGGER_DELAY_DEFAULT = 100
TRIGGER_DELAY_JITTER = "pynput_triggerDelayJitter"
TRIGGER_DELAY_JITTER_DEFAULT = 30
KEY_DELAY = "pynput_stratagemKeyDelay"
KEY_DELAY_DEFAULT = 30
KEY_DELAY_JITTER = "pynput_stratagemKeyDelayJitter"
KEY_DELAY_JITTER_DEFAULT = 20

class PynputExecuter(BaseExecutor):
    def __init__(self, controller):
        super().__init__(controller)
        self.settings = self.controller.get_settings_manager()
        self.keyboard_controller = Controller()
        self.triggerKey = self.parse_macro_key(self.settings.triggerKey)
    
    def on_macro_triggered(self, macro):
        try:
            if macro is not None:
                self.keyboard_controller.press(self.triggerKey)
                utilities.sleepMs(self.triggerDelay, self.triggerDelayJitter)
                for input in macro.commandArray:
                    self.keyboard_controller.press(input)
                    utilities.sleepMs(self.keyDelay, self.keyDelayJitter)
                    self.keyboard_controller.release(input)
                    utilities.sleepMs(self.keyDelay, self.keyDelayJitter)
                self.keyboard_controller.release(self.triggerKey)

        except AttributeError:
            pass
    
    def parse_macro_key(self, key):
        return PynputKeyparser.parse_key(key)
    
    def get_settings_items(self):
        settings = []
        settings.append(SettingsItem("pynput settings", None, None, constants.SETTINGS_VALUE_TYPE_HEADER))
        settings.append(SettingsItem("Trigger delay", TRIGGER_DELAY_DEFAULT, TRIGGER_DELAY, constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Trigger delay jitter", TRIGGER_DELAY_JITTER_DEFAULT, TRIGGER_DELAY_JITTER, constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Stratagem key delay",KEY_DELAY_DEFAULT, KEY_DELAY, constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Stratagem key delay jitter", KEY_DELAY_JITTER_DEFAULT, KEY_DELAY_JITTER, constants.SETTINGS_VALUE_TYPE_INT))

        return settings
    
    def prepare(self):
        self.triggerDelay = getattr(self.settings, TRIGGER_DELAY, TRIGGER_DELAY_DEFAULT)
        self.triggerDelayJitter = getattr(self.settings, TRIGGER_DELAY_JITTER, TRIGGER_DELAY_JITTER_DEFAULT)
        self.keyDelay = getattr(self.settings, KEY_DELAY, KEY_DELAY_DEFAULT)
        self.keyDelayJitter = getattr(self.settings, KEY_DELAY_JITTER, KEY_DELAY_JITTER_DEFAULT)