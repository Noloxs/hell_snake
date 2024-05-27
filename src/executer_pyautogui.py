import pyautogui
from src.executer_base import BaseExecutor
from src import utilities, constants
from src.executer_base import SettingsItem
from src.classes.settings import Settings

TRIGGER_DELAY = "pyautogui_triggerDelay"
TRIGGER_DELAY_JITTER = "pyautogui_triggerDelayJitter"
KEY_DELAY = "pyautogui_stratagemKeyDelay"
KEY_DELAY_JITTER = "pyautogui_stratagemKeyDelayJitter"

class PyAutoGuiExecuter(BaseExecutor):
    def __init__(self):
        super().__init__()
        self.settings = Settings.getInstance()
        pyautogui.FAILSAFE = True
        self.triggerKey = self.parse_macro_key(self.settings.triggerKey)
    
    def on_macro_triggered(self, macro):
        try:
            if macro is not None:
                pyautogui.keyDown(self.triggerKey)
                utilities.sleepMs(self.triggerDelay, self.triggerDelayJitter)
                for input in macro.commandArray:
                    pyautogui.keyDown(input)
                    utilities.sleepMs(self.keyDelay, self.keyDelayJitter)
                    pyautogui.keyUp(input)
                    utilities.sleepMs(self.keyDelay, self.keyDelayJitter)
                pyautogui.keyUp(self.triggerKey)

        except AttributeError:
            pass
    
    def parse_macro_key(self, key):
        return key

    def get_settings_items(self):
        settings = []
        settings.append(SettingsItem("Trigger delay", TRIGGER_DELAY, constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Trigger delay jitter", TRIGGER_DELAY_JITTER, constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Stratagem key delay", KEY_DELAY, constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Stratagem key delay jitter", KEY_DELAY_JITTER, constants.SETTINGS_VALUE_TYPE_INT))

        return settings
    
    def prepare(self):
        self.triggerDelay = getattr(self.settings, TRIGGER_DELAY, 100)
        self.triggerDelayJitter = getattr(self.settings, TRIGGER_DELAY_JITTER, 30)
        self.keyDelay = getattr(self.settings, KEY_DELAY, 30)
        self.keyDelayJitter = getattr(self.settings, KEY_DELAY_JITTER, 20)