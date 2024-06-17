import time
import usb_cdc
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Initialize serial
serial = usb_cdc.data

# Initialize USB HID keyboard
keyboard = Keyboard(usb_hid.devices)

def emulate_key_press(key_char):
    # Convert the key_char to an appropriate keycode if needed
    # This example assumes key_char is a string that maps directly to a key
    if key_char.isalpha():  # For alphabetic characters
        keycode = getattr(Keycode, key_char.upper())
        keyboard.press(keycode)
        keyboard.release_all()
    else:
        # For other characters, you'd need a mapping or handle accordingly
        pass

while True:
    if serial.in_waiting >= 1:  # Wait for at least 3 bytes (1 byte key + 2 bytes delay)
        key_byte = serial.read(1)  # Read 1 byte for the key
        #print("bytes: "+ str(key_byte))
        key = key_byte.decode("utf-8")
        print("key: "+key)
        delay_bytes = serial.read(2)  # Read 2 bytes for the delay
        delay = int.from_bytes(delay_bytes, 'big')  # Convert bytes to integer (big-endian)

        print(str(delay))
        # Emulate the key press
        #emulate_key_press(key)

        # Wait for the specified delay
        #time.sleep(delay / 1000)  # Delay is in milliseconds
