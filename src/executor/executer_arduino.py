import struct
import constants
import utilities
from src.executor.executer_base_serial import SerialBaseExecutor
from src.view.view_base import SettingsItem

EXECUTOR_PREFIX="arduino_"
KEY_DELAY = EXECUTOR_PREFIX+"stratagemKeyDelay"
KEY_DELAY_DEFAULT = 30
KEY_DELAY_JITTER = EXECUTOR_PREFIX+"stratagemKeyDelayJitter"
KEY_DELAY_JITTER_DEFAULT = 20
TRIGGER_DELAY = EXECUTOR_PREFIX+"triggerKeyDelay"
TRIGGER_DELAY_DEFAULT = 100
TRIGGER_DELAY_JITTER = EXECUTOR_PREFIX+"triggerKeyDelayJitter"
TRIGGER_DELAY_JITTER_DEFAULT = 30

class ArduinoPassthroughExecuter(SerialBaseExecutor):
    def __init__(self, controller):
        super().__init__(controller)
        self.settings = self.controller.get_settings_manager()

    def get_executor_prefix(self):
        return EXECUTOR_PREFIX
    
    def on_macro_triggered(self, macro):
        #Sending a negative number indicates that the key should be pressed but not released
        hexToSend = self.triggerKey + self.delay_to_hex(int(utilities.getDelayWithJitterMs(self.triggerDelay, self.triggerDelayJitter))*-1) # Trigger stratagem
        for key in macro.commandArray:
            hexToSend += str(key) # Key press
            hexToSend += self.delay_to_hex(int(utilities.getDelayWithJitterMs(self.keyDelay, self.keyDelayJitter))) # Key press delay
        hexToSend += self.triggerKey + self.delay_to_hex(int(utilities.getDelayWithJitterMs(self.triggerDelay, self.triggerDelayJitter))) # Release trigger

        self.send_bytes(bytes.fromhex(hexToSend))

    def get_settings_items(self):
        settings = []
        settings.append(SettingsItem("Arduino passthrough settings", None, None, constants.SETTINGS_VALUE_TYPE_HEADER))
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

    def parse_to_hex(self, key):
        return hex(ord(key))[2:]

    def delay_to_hex(self, delay):
        # Ensure the delay fits into a 2-byte (16-bit) signed integer
        if not -32768 <= delay <= 32767:
            raise ValueError("Number out of range for 2-byte signed integer")

        # Pack the delay as a 2-byte signed integer
        packed_delay = struct.pack('>h', delay)  # '>h' means big-endian 2-byte signed integer

        # Convert the packed bytes to hexadecimal representation for display (optional)
        hex_representation = packed_delay.hex()
        return hex_representation
    
    def parse_macro_key(self, key):   
        if key in self.key_map:
            return self.key_map[key]
        else:
            return self.parse_to_hex(key)

    key_map = {
        "shift":"81",
        "ctrl":"80",
        "up":"DA",
        "down":"D9",
        "left":"D8",
        "right":"D7",
        "caps_lock":"C1"
        } 