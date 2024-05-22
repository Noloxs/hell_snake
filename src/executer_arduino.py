from src.executer_base import BaseExecutor
import serial.tools.list_ports
from src import utilities

START_HEX = "fb"
TERMINATION_HEX = "f7"
SEPERATOR_HEX = "fa"
HOLD_KEY_HEX = "f8"
RELEASE_KEY_HEX = "f9"

class ArduinoPassthroughExecuter(BaseExecutor):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.arduino = None
        self.triggerKey = self.parse_macro_key(self.model.settings.triggerKey)

    def connect_to_arduino(self, port):
        self.arduino = serial.Serial(port, baudrate=115200, timeout=.1)
        # TODO Send connection test message
    
    def on_macro_triggered(self, macro):
        hexToSend = START_HEX
        hexToSend += self.triggerKey + SEPERATOR_HEX + HOLD_KEY_HEX + SEPERATOR_HEX # Trigger strat
        for key in macro.commandArray:
            hexToSend += str(key) + SEPERATOR_HEX # Key press
            hexToSend += self.delay_to_hex(int(utilities.getStratagemKeyDelayMs(self.model))) + SEPERATOR_HEX  # Key press delay
        hexToSend += self.triggerKey + SEPERATOR_HEX + RELEASE_KEY_HEX + SEPERATOR_HEX
        hexToSend += TERMINATION_HEX

        self.send_bytes(bytes.fromhex(hexToSend))

    def send_bytes(self, bytes):
        if self.arduino is not None:
            self.arduino.write(bytes)

    def parse_to_hex(self, key):
        return hex(ord(key))[2:]

    def delay_to_hex(self, delay):
        # Handle delays outside of range
        return hex(delay)[2:]
    
    def get_physical_addresses(self):
        ports = serial.tools.list_ports.comports()
        return ports
    
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