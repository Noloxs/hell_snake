import time
import usb_cdc
import usb_hid
import binascii
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Initialize serial
serial = usb_cdc.data

# Initialize USB HID keyboard
keyboard = Keyboard(usb_hid.devices)

def unsigned_to_signed(unsigned_val):
    # Ensure the input is within the range of a 2-byte unsigned integer
    if not (0 <= unsigned_val <= 0xFFFF):
        raise ValueError("Input should be a 2-byte unsigned integer (0 to 65535)")

    # If the value is greater than the maximum for a signed 2-byte integer, convert it
    if unsigned_val > 0x7FFF:  # 32767 in decimal
        return unsigned_val - 0x10000  # 65536 in decimal
    else:
        return unsigned_val

while True:
    if serial.in_waiting >= 3:  # Wait for at least 3 bytes (1 byte key + 2 bytes delay)
        key_byte = int.from_bytes(serial.read(1), 'big')  # Read 1 byte for the key
        keyboard.press(int(key_byte))
        
        delay_bytes = serial.read(2)  # Read 2 bytes for the delay
        delay = unsigned_to_signed(int.from_bytes(delay_bytes, 'big'))  # Convert bytes to signed integer (big-endian)
        time.sleep(abs(delay)/1000)
        
        if delay >= 0:
            keyboard.release(int(key_byte))
