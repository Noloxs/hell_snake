from src.executer_base import BaseExecutor
import serial.tools.list_ports
from src import utilities, constants
from src.view.view_base import SettingsItem, MenuItem
from src.classes.settings import Settings
import struct

KEY_DELAY = "pico_stratagemKeyDelay"
KEY_DELAY_DEFAULT = 30
KEY_DELAY_JITTER = "pico_stratagemKeyDelayJitter"
KEY_DELAY_JITTER_DEFAULT = 20
TRIGGER_DELAY = "pico_triggerKeyDelay"
TRIGGER_DELAY_DEFAULT = 100
TRIGGER_DELAY_JITTER = "pico_triggerKeyDelayJitter"
TRIGGER_DELAY_JITTER_DEFAULT = 30
KEY_LAST_CONNECTED = "pico_lastConnectedDevice"
KEY_LAST_CONNECTED_DEFAULT = None
KEY_AUTO_RECONNECT = "pico_autoReconnect"
KEY_AUTO_RECONNECT_DEFAULT = True

class PicoPassthroughExecuter(BaseExecutor):
    def __init__(self, controller):
        super().__init__()
        self.pico = None
        self.settings = Settings.getInstance()
        self.controller = controller

    def start(self):
        if getattr(self.settings, KEY_AUTO_RECONNECT, KEY_AUTO_RECONNECT_DEFAULT):
            self.attempt_auto_connect()
        self.prepare()

    def stop(self):
        if self.pico is not None:
            self.pico.close()
            self.pico = None

    def attempt_auto_connect(self):
        last_connected = getattr(self.settings, KEY_LAST_CONNECTED, KEY_LAST_CONNECTED_DEFAULT)
        if last_connected is not None:
            ports = self.get_physical_addresses()
            for port in ports:
                id = str(port.vid)+"-"+str(port.pid)
                if id == last_connected:
                    self.connect_to_pico(port)
                    return

    def connect_to_pico(self, port):
        # Ensure any existing serial connection is properly closed before establishing a new one
        if self.pico is not None:
            self.pico.close()
            self.pico = None

        self.pico = serial.Serial(port.device, baudrate=115200, timeout=.1)
        self.controller.update_executor_menu()
        setattr(self.settings, KEY_LAST_CONNECTED, str(port.vid) + "-" + str(port.pid))
        self.controller.update_title_description("Connected to: " + port.name)

        # TODO Send connection test message
    
    def on_macro_triggered(self, macro):
        #Sending a negative number indicates that the key should be pressed but not released
        bytesToSend = self.triggerKey.encode('utf-8') + int(utilities.getDelayWithJitterMs(self.triggerDelay, self.triggerDelayJitter)*-1).to_bytes(2, 'big', signed = True) # Trigger stratagem
        for key in macro.commandArray:
            bytesToSend += key.encode('utf-8') # Key press
            bytesToSend += int(utilities.getDelayWithJitterMs(self.keyDelay, self.keyDelayJitter)).to_bytes(2,'big', signed = True) # Key press delay
        bytesToSend += self.triggerKey.encode('utf-8') + int(utilities.getDelayWithJitterMs(self.triggerDelay, self.triggerDelayJitter)).to_bytes(2, 'big', signed = True) # Release trigger

        bytesToSend = bytes.fromhex("04")

        self.send_bytes(bytesToSend)

    def get_menu_items(self):
        menu_items = []

        select_serial = MenuItem("Select serial", None, None, constants.MENU_TYPE_MENU)
        connection = self.get_current_connection()
        physical_addresses = self.get_physical_addresses()
        for port in sorted(physical_addresses):
            if port.device == connection:
                icon = constants.ICON_BASE_PATH+"serial_connected"
            else:
                icon = None
            select_serial.children.append(MenuItem(port.description, icon, lambda checked, port=port: self.connect_to_pico(port), constants.MENU_TYPE_ACTION))

        menu_items.append(select_serial)

        return menu_items

    def get_settings_items(self):
        settings = []
        settings.append(SettingsItem("Pico passthrough settings", None, None, constants.SETTINGS_VALUE_TYPE_HEADER))
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
        print(bytes)
        if self.pico is not None:
            self.pico.write(bytes)

    def get_physical_addresses(self):
        ports = serial.tools.list_ports.comports()
        return ports
    
    def get_current_connection(self):
        if self.pico is None:
            return None
        else:
            return self.pico.port
    
    def parse_macro_key(self, key):   
        if key in self.key_map:
            return self.key_map[key]
        else:
            return key

    key_map = {
        "shift":"a",
        "ctrl":"b",
        "up":"c",
        "down":"d",
        "left":"e",
        "right":"f",
        "caps_lock":"g"
        } 