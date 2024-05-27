import pyautogui
from src.executer_base import BaseExecutor
from src import utilities, constants
from src.executer_base import SettingsItem

class PyAutoGuiExecuter(BaseExecutor):
    def __init__(self, model):
        super().__init__()
        self.model = model
        pyautogui.FAILSAFE = True
        self.triggerKey = self.parse_macro_key(self.model.settings.triggerKey)
    
    def on_macro_triggered(self, macro):
        try:
            if macro is not None:
                pyautogui.keyDown(self.triggerKey)
                utilities.sleepTriggerKey(self.model)
                for input in macro.commandArray:
                    pyautogui.keyDown(input)
                    utilities.sleepStratagemKey(self.model)
                    pyautogui.keyUp(input)
                    utilities.sleepStratagemKey(self.model)
                pyautogui.keyUp(self.triggerKey)

        except AttributeError:
            pass
    
    def parse_macro_key(self, key):
        return key

    def get_settings_items(self):
        settings = []
        # TODO Update settings keys to be executor exclusive
        settings.append(SettingsItem("Trigger delay", "triggerDelay", constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Trigger delay jitter", "triggerDelayJitter", constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Stratagem key delay", "stratagemKeyDelay", constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Stratagem key delay jitter", "stratagemKeyDelayJitter", constants.SETTINGS_VALUE_TYPE_INT))

        return settings