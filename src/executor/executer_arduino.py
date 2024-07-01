import struct
import constants
import utilities
import serial
from src.executor.executer_base import BaseExecutor
from src.view.view_base import SettingsItem, MenuItem
from src.executor.executer_utilities import ExecuterUtilities

KEY_DELAY = "arduino_stratagemKeyDelay"
KEY_DELAY_DEFAULT = 30
KEY_DELAY_JITTER = "arduino_stratagemKeyDelayJitter"
KEY_DELAY_JITTER_DEFAULT = 20
TRIGGER_DELAY = "arduino_triggerKeyDelay"
TRIGGER_DELAY_DEFAULT = 100
TRIGGER_DELAY_JITTER = "arduino_triggerKeyDelayJitter"
TRIGGER_DELAY_JITTER_DEFAULT = 30
KEY_LAST_CONNECTED = "arduino_lastConnectedDevice"
KEY_LAST_CONNECTED_DEFAULT = None
KEY_AUTO_RECONNECT = "arduino_autoReconnect"
KEY_AUTO_RECONNECT_DEFAULT = True

class ArduinoPassthroughExecuter(BaseExecutor):
    def __init__(self, controller):
        super().__init__(controller)
        self.arduino = None
        self.settings = self.controller.get_settings_manager()

    def start(self):
        if getattr(self.settings, KEY_AUTO_RECONNECT, KEY_AUTO_RECONNECT_DEFAULT):
            self.attempt_auto_connect()
        self.prepare()

    def stop(self):
        if self.arduino is not None:
            self.arduino.close()
            self.arduino = None

    def attempt_auto_connect(self):
        if getattr(self.settings, KEY_LAST_CONNECTED, KEY_LAST_CONNECTED_DEFAULT) is not None:
            ports = ExecuterUtilities.get_physical_addresses()
            for port in ports:
                id = str(port.vid)+"-"+str(port.pid)
                if id == self.settings.arduino_lastConnectedDevice:
                    self.connect_to_arduino(port)
                    return

    def connect_to_arduino(self, port):
        # Ensure any existing serial connection is properly closed before establishing a new one
        if self.arduino is not None:
            self.arduino.close()
            self.arduino = None

        self.arduino = serial.Serial(port.device, baudrate=115200, timeout=.1)
        self.controller.update_executor_menu()
        setattr(self.settings, KEY_LAST_CONNECTED, str(port.vid) + "-" + str(port.pid))
        self.controller.update_title_description("Connected to: " + port.name)

        # TODO Send connection test message
    
    def on_macro_triggered(self, macro):
        #Sending a negative number indicates that the key should be pressed but not released
        hexToSend = self.triggerKey + self.delay_to_hex(int(utilities.getDelayWithJitterMs(self.triggerDelay, self.triggerDelayJitter))*-1) # Trigger stratagem
        for key in macro.commandArray:
            hexToSend += str(key) # Key press
            hexToSend += self.delay_to_hex(int(utilities.getDelayWithJitterMs(self.keyDelay, self.keyDelayJitter))) # Key press delay
        hexToSend += self.triggerKey + self.delay_to_hex(int(utilities.getDelayWithJitterMs(self.triggerDelay, self.triggerDelayJitter))) # Release trigger

        self.send_bytes(bytes.fromhex(hexToSend))

    def get_menu_items(self):
        menu_items = []

        select_serial = MenuItem("Select serial", None, None, constants.MENU_TYPE_MENU)
        connection = self.get_current_connection()
        physical_addresses = ExecuterUtilities.get_physical_addresses()
        for port in sorted(physical_addresses):
            if port.device == connection:
                icon = constants.ICON_BASE_PATH+"serial_connected"
            else:
                icon = None
            select_serial.children.append(MenuItem(port.description, icon, lambda checked, port=port: self.connect_to_arduino(port), constants.MENU_TYPE_ACTION))

        menu_items.append(select_serial)

        return menu_items

    def get_settings_items(self):
        settings = []
        settings.append(SettingsItem("Arduino passthrough settings", None, None, constants.SETTINGS_VALUE_TYPE_HEADER))
        settings.append(SettingsItem("Trigger delay", TRIGGER_DELAY_DEFAULT, TRIGGER_DELAY, constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Trigger delay jitter", TRIGGER_DELAY_JITTER_DEFAULT, TRIGGER_DELAY_JITTER, constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Stratagem key delay", KEY_DELAY_DEFAULT, KEY_DELAY, constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Stratagem key delay jitter", KEY_DELAY_JITTER_DEFAULT, KEY_DELAY_JITTER, constants.SETTINGS_VALUE_TYPE_INT))
        settings.append(SettingsItem("Hardware Connection", None, None, constants.SETTINGS_VALUE_TYPE_HEADER))
        settings.append(SettingsItem("Auto re-connect to latest device", KEY_AUTO_RECONNECT_DEFAULT, KEY_AUTO_RECONNECT, constants.SETTINGS_VALUE_TYPE_BOOL))

        return settings

    def prepare(self):
        self.triggerKey = self.parse_macro_key(self.settings.triggerKey)
        self.keyDelay = getattr(self.settings, KEY_DELAY, KEY_DELAY_DEFAULT)
        self.keyDelayJitter = getattr(self.settings, KEY_DELAY_JITTER, KEY_DELAY_JITTER_DEFAULT)
        self.triggerDelay = getattr(self.settings, TRIGGER_DELAY, TRIGGER_DELAY_DEFAULT)
        self.triggerDelayJitter = getattr(self.settings, TRIGGER_DELAY_JITTER, TRIGGER_DELAY_JITTER_DEFAULT)

    def send_bytes(self, bytes):
        if self.arduino is not None:
            self.arduino.write(bytes)

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
    
    def get_current_connection(self):
        if self.arduino is None:
            return None
        else:
            return self.arduino.port # TODO How to get port from serial
    
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