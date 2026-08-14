import time
import usb_cdc
import usb_hid
import gc
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Initialize serial
serial = usb_cdc.data

# Initialize USB HID keyboard
keyboard = Keyboard(usb_hid.devices)

# Pre-allocate a buffer for reading serial data to avoid allocations in the loop
buffer = bytearray(3)

# Idle state variables
last_activity_time = time.monotonic()
inactivity_threshold = 900  # 15 minutes in seconds
is_sleeping = True

def unsigned_to_signed(unsigned_val):
    # If the value is greater than the maximum for a signed 2-byte integer, convert it
    if unsigned_val > 0x7FFF:  # 32767 in decimal
        return unsigned_val - 0x10000  # 65536 in decimal
    else:
        return unsigned_val

def process_command(command_byte, parameter_byte):
    """
    Processes special commands received via serial.
    """
    global last_activity_time, is_sleeping
    if command_byte == 0x01:  # Wakeup command
        last_activity_time = time.monotonic() # Reset activity timer
        is_sleeping = False
    # Add more command cases here as needed

def process_serial_input(serial_obj, keyboard_obj, data_buffer):
    """
    Processes a single serial input message to simulate a key press or handle a command.
    Assumes 3 bytes are available in serial_obj: 1 for key_code/command, 2 for delay/parameter.
    """
    global last_activity_time, is_sleeping
    serial_obj.readinto(data_buffer)  # Read 3 bytes into the buffer

    first_byte = data_buffer[0]

    if first_byte == 0x00:  # Special command mode
        command_byte = data_buffer[1]
        parameter_byte = data_buffer[2]
        process_command(command_byte, parameter_byte)
    else:
        key_code = first_byte
        
        # Combine the next two bytes for the delay and convert to a signed integer
        delay_unsigned = (data_buffer[1] << 8) | data_buffer[2]
        delay_signed = unsigned_to_signed(delay_unsigned)
        
        keyboard_obj.press(key_code)
        
        # Calculate sleep time in seconds
        sleep_duration = abs(delay_signed) / 1000.0
        time.sleep(sleep_duration)
        
        if delay_signed >= 0:
            keyboard_obj.release(key_code)
            # The original Arduino code has a second delay here.
            # If timing issues persist, uncommenting the following line might help.
            # time.sleep(sleep_duration)

    # Update activity time on any serial input
    last_activity_time = time.monotonic()
    is_sleeping = False

    # Manually run garbage collection to have more control over when it happens
    gc.collect()

def handle_idle_state(keyboard_obj):
    """
    Checks for inactivity and puts the device into an idle/sleep state.
    """
    global last_activity_time, is_sleeping
    if time.monotonic() - last_activity_time > inactivity_threshold:
        if not is_sleeping:
            keyboard_obj.release_all() # Release all pressed keys
            is_sleeping = True
        time.sleep(1) # Sleep for a short period to save power
    else:
        time.sleep(0.005) # Short delay during active operation

if __name__ == "__main__":
    while True:
        if serial.in_waiting >= 3:  # Wait for at least 3 bytes
            process_serial_input(serial, keyboard, buffer)
        else:
            handle_idle_state(keyboard)
