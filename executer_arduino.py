import time
import serial
import random
from executer_base import BaseExecutor
import serial.tools.list_ports
from config import strategemTriggerKey, triggerDelayMax, triggerDelayMin

class ArduinoPassthroughExecuter(BaseExecutor):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def connect_to_arduino(self, port):
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            print("{}: {} [{}]".format(port, desc, hwid))

        self.arduino = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=.1)
        # TODO Send connection test message
    
    def on_macro_triggered(self, macro):
        # TODO Convert macro to bytes to send
        #                             start shift hold k 50 k 50 i 50 l 50 shift release end
        self.send_bytes(bytes.fromhex("fb 81fa f8fa 6bfa 32fa 6bfa 32fa 69fa 32fa 6cfa 32fa 81fa f9fa f7"))

    def send_bytes(self, bytes):
        self.arduino.write(bytes)

    def add_settings(self, overview):
        # TODO Add dropdown to select external device
        pass