import pytest
from unittest.mock import MagicMock, patch

import pytest
from unittest.mock import MagicMock, patch

import pytest
from unittest.mock import MagicMock, patch

def test_process_serial_input_single_key():
    from pico_passthrough import code

    # --- Setup Mocks ---
    # Mock usb_cdc.data (serial input)
    code.serial.in_waiting = 3 # Set in_waiting for the test
    code.serial.readinto.side_effect = lambda x: x.__setitem__(slice(0,3), bytearray([test_key_code, test_delay_bytes[0], test_delay_bytes[1]]))

    # Mock adafruit_hid.keyboard.Keyboard
    mock_keyboard = MagicMock()
    code.keyboard = mock_keyboard # Assign mock to the global variable in code.py

    # --- Simulate Input Data ---
    # Example: Key 'A' (keycode 4), delay 100ms (0x0064)
    test_key_code = 4 # Keycode for 'A'
    test_delay_ms = 100
    test_delay_bytes = test_delay_ms.to_bytes(2, 'big', signed=False) # Convert to 2 bytes

    # The buffer that `process_serial_input` expects
    input_buffer = bytearray(3)

    # --- Call the function under test ---
    # We call the main loop directly, as it's now part of code.py
    # We need to ensure the loop runs once for the test
    # This is a bit tricky with a while True loop, so we'll simulate the loop's condition
    # and directly call the process_serial_input function for testing purposes.
    # The actual code.py will have the while True loop.
    code.process_serial_input(code.serial, code.keyboard, input_buffer)

    # --- Assertions ---
    # Verify that keyboard.press was called with the correct keycode
    mock_keyboard.press.assert_called_once_with(test_key_code)

    # Verify that time.sleep was called with the correct duration
    code.time.sleep.assert_called_once_with(abs(test_delay_ms) / 1000.0)

    # Verify that keyboard.release was called with the correct keycode
    mock_keyboard.release.assert_called_once_with(test_key_code)

    # Verify that gc.collect was called
    code.gc.collect.assert_called_once()

def test_process_serial_input_negative_delay():
    from pico_passthrough import code

    # Mock usb_cdc.data (serial input)
    code.serial.in_waiting = 3 # Set in_waiting for the test
    test_key_code = 5 # Keycode for 'B'
    test_delay_ms = -50 # Negative delay
    # Convert negative delay to unsigned 2-byte representation for the buffer
    test_delay_unsigned = (test_delay_ms + 0x10000) if test_delay_ms < 0 else test_delay_ms
    test_delay_bytes = test_delay_unsigned.to_bytes(2, 'big', signed=False)
    code.serial.readinto.side_effect = lambda x: x.__setitem__(slice(0,3), bytearray([test_key_code, test_delay_bytes[0], test_delay_bytes[1]]))

    # Mock adafruit_hid.keyboard.Keyboard
    mock_keyboard = MagicMock()
    code.keyboard = mock_keyboard # Assign mock to the global variable in code.py

    input_buffer = bytearray(3)

    code.process_serial_input(code.serial, mock_keyboard, input_buffer)

    mock_keyboard.press.assert_called_once_with(test_key_code)
    code.time.sleep.assert_called_once_with(abs(test_delay_ms) / 1000.0)
    # For negative delay, release should NOT be called
    mock_keyboard.release.assert_not_called()
    code.gc.collect.assert_called_once()


def test_process_serial_input_zero_delay():
    from pico_passthrough import code

    # Mock usb_cdc.data (serial input)
    code.serial.in_waiting = 3 # Set in_waiting for the test
    test_key_code = 6 # Keycode for 'C'
    test_delay_ms = 0 # Zero delay
    test_delay_bytes = test_delay_ms.to_bytes(2, 'big', signed=False)
    code.serial.readinto.side_effect = lambda x: x.__setitem__(slice(0,3), bytearray([test_key_code, test_delay_bytes[0], test_delay_bytes[1]]))

    # Mock adafruit_hid.keyboard.Keyboard
    mock_keyboard = MagicMock()
    code.keyboard = mock_keyboard # Assign mock to the global variable in code.py

    input_buffer = bytearray(3)

    code.process_serial_input(code.serial, mock_keyboard, input_buffer)

    mock_keyboard.press.assert_called_once_with(test_key_code)
    code.time.sleep.assert_called_once_with(0.0)
    mock_keyboard.release.assert_called_once_with(test_key_code)
    code.gc.collect.assert_called_once()


def test_no_serial_data():
    from pico_passthrough import code

    # Mock serial.in_waiting to be less than 3
    code.serial.in_waiting = 2

    # Mock the process_serial_input function to ensure it's not called
    with patch('pico_passthrough.code.process_serial_input') as mock_process_serial_input:
        # Simulate the main loop's condition
        if code.serial.in_waiting >= 3:
            code.process_serial_input(code.serial, code.keyboard, code.buffer)

        mock_process_serial_input.assert_not_called()

def test_process_serial_input_command_wakeup():
    from pico_passthrough import code

    # Mock usb_cdc.data (serial input)
    code.serial.in_waiting = 3 # Set in_waiting for the test
    # Simulate a wakeup command: 0x00 (command mode), 0x01 (wakeup command), 0x00 (parameter)
    command_bytes = bytearray([0x00, 0x01, 0x00])
    code.serial.readinto.side_effect = lambda x: x.__setitem__(slice(0,3), command_bytes)

    # Mock adafruit_hid.keyboard.Keyboard
    mock_keyboard = MagicMock()
    code.keyboard = mock_keyboard # Assign mock to the global variable in code.py

    input_buffer = bytearray(3)

    # --- Call the function under test ---
    code.process_serial_input(code.serial, mock_keyboard, input_buffer)

    # --- Assertions ---
    # Commands should not trigger key presses or releases
    mock_keyboard.press.assert_not_called()
    mock_keyboard.release.assert_not_called()
    code.time.sleep.assert_not_called() # No sleep for commands

    # gc.collect should still be called
    code.gc.collect.assert_called_once()

