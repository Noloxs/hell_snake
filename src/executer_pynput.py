from pynput.keyboard import Controller
from src.executer_base import BaseExecutor
from src import utilities, key_parser_pynput, constants
from src.executer_base import SettingsItem

class PynputExecuter(BaseExecutor):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.keyboard_controller = Controller()
        self.triggerKey = self.parse_macro_key(self.model.settings.triggerKey)
    
    def on_macro_triggered(self, macro):
        try:
            if macro is not None:
                self.keyboard_controller.press(self.triggerKey)
                utilities.sleepTriggerKey(self.model)
                for input in macro.commandArray:
                    self.keyboard_controller.press(input)
                    utilities.sleepStratagemKey(self.model)
                    self.keyboard_controller.release(input)
                    utilities.sleepStratagemKey(self.model)
                self.keyboard_controller.release(self.triggerKey)

        except AttributeError:
            pass
    
    def parse_macro_key(self, key):
        return key_parser_pynput.parse_key(key)
    
    def get_settings_items(self):
        settings = []
        # TODO Update settings keys to be executor exclusive
        settings.append(SettingsItem("Trigger delay", "triggerDelay", constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Trigger delay jitter", "triggerDelayJitter", constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Stratagem key delay", "stratagemKeyDelay", constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Stratagem key delay jitter", "stratagemKeyDelayJitter", constants.SETTINGS_VALUE_TYPE_INT))

        return settings