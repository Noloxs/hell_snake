from src.executor.executer_base_serial import SerialBaseExecutor
import utilities
import constants
from src.view.view_base import SettingsItem

EXECUTOR_PREFIX = "pico_"
KEY_DELAY = EXECUTOR_PREFIX+"stratagemKeyDelay"
KEY_DELAY_DEFAULT = 30
KEY_DELAY_JITTER = EXECUTOR_PREFIX+"stratagemKeyDelayJitter"
KEY_DELAY_JITTER_DEFAULT = 20
TRIGGER_DELAY = EXECUTOR_PREFIX+"triggerKeyDelay"
TRIGGER_DELAY_DEFAULT = 100
TRIGGER_DELAY_JITTER = EXECUTOR_PREFIX+"triggerKeyDelayJitter"
TRIGGER_DELAY_JITTER_DEFAULT = 30

class PicoPassthroughExecuter(SerialBaseExecutor):
    def __init__(self, controller):
        super().__init__(controller)
        self.pico = None
        self.settings = controller.get_settings_manager()

    def get_executor_prefix(self):
        return EXECUTOR_PREFIX

    def on_macro_triggered(self, macro):
        #Sending a negative number indicates that the key should be pressed but not released
        bytesToSend = bytes.fromhex(self.triggerKey) + int(utilities.getDelayWithJitterMs(self.triggerDelay, self.triggerDelayJitter)*-1).to_bytes(2, 'big', signed = True) # Trigger stratagem
        for key in macro.commandArray:
            bytesToSend += bytes.fromhex(key) # Key press
            bytesToSend += int(utilities.getDelayWithJitterMs(self.keyDelay, self.keyDelayJitter)).to_bytes(2,'big', signed = True) # Key press delay
        bytesToSend += bytes.fromhex(self.triggerKey) + int(utilities.getDelayWithJitterMs(self.triggerDelay, self.triggerDelayJitter)).to_bytes(2, 'big', signed = True) # Release trigger

        self.send_bytes(bytesToSend)

    def get_settings_items(self):
        settings = []
        settings.append(SettingsItem("Pico passthrough settings", None, None, constants.SETTINGS_VALUE_TYPE_HEADER))
        settings.append(SettingsItem("Trigger delay", TRIGGER_DELAY_DEFAULT, TRIGGER_DELAY, constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Trigger delay jitter", TRIGGER_DELAY_JITTER_DEFAULT, TRIGGER_DELAY_JITTER, constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Stratagem key delay", KEY_DELAY_DEFAULT, KEY_DELAY, constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Stratagem key delay jitter", KEY_DELAY_JITTER_DEFAULT, KEY_DELAY_JITTER, constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Hardware Connection", None, None, constants.SETTINGS_VALUE_TYPE_HEADER))
        settings.extend(SerialBaseExecutor.get_settings_items(self))

        return settings

    def prepare(self):
        self.triggerKey = self.parse_macro_key(self.settings.triggerKey)
        self.keyDelay = getattr(self.settings, KEY_DELAY, KEY_DELAY_DEFAULT)
        self.keyDelayJitter = getattr(self.settings, KEY_DELAY_JITTER, KEY_DELAY_JITTER_DEFAULT)
        self.triggerDelay = getattr(self.settings, TRIGGER_DELAY, TRIGGER_DELAY_DEFAULT)
        self.triggerDelayJitter = getattr(self.settings, TRIGGER_DELAY_JITTER, TRIGGER_DELAY_JITTER_DEFAULT)

    def send_bytes(self, bytes):
        if self.pico is not None:
            self.pico.write(bytes)
    
    def parse_macro_key(self, key):
        if key in self.key_map:
            return self.key_map[key]
        else:
            print("Does not support: "+str(key))
            raise KeyError

    key_map = {
        "a":"04",
        "b":"05",
        "c":"06",
        "d":"07",
        "e":"08",
        "f":"09",
        "g":"0A",
        "h":"0B",
        "i":"0C",
        "j":"0D",
        "k":"0E",
        "l":"0F",
        "m":"10",
        "n":"11",
        "o":"12",
        "p":"13",
        "q":"14",
        "r":"15",
        "s":"16",
        "t":"17",
        "u":"18",
        "v":"19",
        "w":"1A",
        "x":"1B",
        "y":"1C",
        "z":"1D",
        "1":"1E",
        "2":"1F",
        "3":"20",
        "4":"21",
        "5":"22",
        "6":"23",
        "7":"24",
        "8":"25",
        "9":"26",
        "0":"27",
        "shift":"E1",
        "ctrl":"E0",
        "up":"52",
        "down":"51",
        "left":"50",
        "right":"4F",
        "caps_lock":"39"
        } 