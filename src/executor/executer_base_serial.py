import constants
from abc import abstractmethod
import serial
from src.executor.executer_base import BaseExecutor
from src.view.view_base import MenuItem
from src.executor.executer_utilities import ExecuterUtilities
from src.view.view_base import SettingsItem
from src.executor.exceptions import ExecutorErrorException

KEY_LAST_CONNECTED_DEFAULT = None
AUTO_RECONNECT = "autoReconnect"
KEY_AUTO_RECONNECT_DEFAULT = True

class SerialBaseExecutor(BaseExecutor):
    def __init__(self, controller):
        super().__init__(controller)
        self.EXECUTOR_PREFIX = self.get_executor_prefix()
        self.KEY_LAST_CONNECTED_DEVICE = self.EXECUTOR_PREFIX+"lastConnectedDevice"
        self.KEY_AUTO_RECONNECT =  self.EXECUTOR_PREFIX+AUTO_RECONNECT
        self.usb_device = None
        self.settings = self.controller.get_settings_manager()
    
    def start(self):
        if getattr(self.settings, self.KEY_AUTO_RECONNECT, KEY_AUTO_RECONNECT_DEFAULT):
            self.attempt_auto_connect()
            self.send_wakeup()
        self.prepare()

    def send_wakeup(self):
        # Send a wakeup command
        cmd = bytearray([0x00, 0x01, 0x00])
        self.send_bytes(cmd)

    def stop(self):
        if self.usb_device is not None:
            self.usb_device.close()
            self.usb_device = None

    def send_bytes(self, bytes):
        if self.usb_device is not None:
            try:
                self.usb_device.write(bytes)
            except serial.SerialException as e:
                # Handle the exception, maybe log it or notify the user
                raise ExecutorErrorException("Error sending bytes to serial port: " + str(e))

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
            select_serial.children.append(MenuItem(port.description, icon, lambda checked, port=port: self.connect_to_device(port), constants.MENU_TYPE_ACTION))
        
        #Add re-scan for serial button
        select_serial.children.append(MenuItem("","","",constants.MENU_TYPE_SEPARATOR))
        select_serial.children.append(MenuItem("Scan for devices", constants.ICON_BASE_PATH+"settings_refresh_devices", lambda checked : self.controller.update_executor_menu(), constants.MENU_TYPE_ACTION))

        menu_items.append(select_serial)
        return menu_items

    def attempt_auto_connect(self):
        last_connected = getattr(self.settings, self.KEY_LAST_CONNECTED_DEVICE, KEY_LAST_CONNECTED_DEFAULT)
        if last_connected is not None:
            ports = ExecuterUtilities.get_physical_addresses()
            for port in ports:
                id = str(port.vid)+"-"+str(port.pid)
                if id == last_connected:
                    self.connect_to_device(port)
                    return
    
    def connect_to_device(self, port):
        # Ensure any existing serial connection is properly closed before establishing a new one
        if self.usb_device is not None:
            self.usb_device.close()
            self.usb_device = None

        try:
            self.usb_device = serial.Serial(port.device, baudrate=115200, timeout=.1, write_timeout=0.2)
            print("Connected to: " + port.name)
        except serial.SerialException as e:
            # Handle the exception, maybe log it or notify the user
            raise ExecutorErrorException("Failed to open serial port: " + str(e))

        # If no exception occurred, proceed with updating the executor menu
        self.controller.update_executor_menu()
        setattr(self.settings, self.KEY_LAST_CONNECTED_DEVICE, str(port.vid) + "-" + str(port.pid))
        self.controller.update_title_description("Connected to: " + port.name)

        # TODO Send connection test message
    
    def get_current_connection(self):
        if self.usb_device is None:
            return None
        else:
            return self.usb_device.port # TODO How to get port from serial

    def get_settings_items(self):
        settings = []
        settings.append(SettingsItem("Auto re-connect to latest device", KEY_AUTO_RECONNECT_DEFAULT, self.KEY_AUTO_RECONNECT, constants.SETTINGS_VALUE_TYPE_BOOL))

        return settings

    @abstractmethod
    def get_executor_prefix(self):
        raise NotImplementedError