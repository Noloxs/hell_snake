# Pico Passthrough TODO

This document outlines tasks for improving the `pico_passthrough` code, including feature parity with the Arduino version and enhancing testability.

## Feature Parity with Arduino

1. [x] **Implement Idle/Sleep Mode:**
    1.1. [x] Detect inactivity (e.g., no serial input for a defined period).
    1.2. [x] Enter a low-power state or release all keys when idle.
    1.3. [x] Wake up upon receiving new serial input.
    1.4. [x] Consider using `supervisor.runtime.ticks_ms()` for inactivity tracking if `time.monotonic()` is not suitable for long periods.
2. [x] **Add Special Command Handling:**
    2.1. [x] Define a protocol for special commands (e.g., a specific byte sequence to indicate a command rather than a key press).
    2.2. [x] Implement handlers for commands like "wakeup" or other future control signals.

## Enhancing Testability

3. [x] **Refactor `code.py` for Unit Testing:**
    3.1. [x] Extract the core logic of the `while True` loop into a testable function (e.g., `process_serial_input(serial_data, keyboard_obj)`).
    3.2. [x] This function should take dependencies (like `serial` and `keyboard` objects) as arguments, rather than relying on global imports, to facilitate mocking.
    3.3. [x] Ensure the function processes a single "message" or set of inputs per call.
4. [x] **Set up Mocking for Hardware Dependencies:**
    4.1. [x] Create mock objects for `usb_cdc.data` (to simulate serial input) and `adafruit_hid.keyboard.Keyboard` (to capture key press/release calls).
    4.2. [x] Use Python's `unittest.mock` or `pytest-mock` for this purpose.
5. [x] **Write Unit Tests:**
    5.1. [x] Create a `tests/test_pico_code.py` file.
    5.2. [x] Write test cases to cover:
        5.2.1. [x] Single key presses with various delays (positive and negative).
        5.2.2. [x] Edge cases for delay values (e.g., zero delay).
        5.2.3. [x] Behavior when no serial data is available (after implementing idle mode).
        5.2.4. [x] Special command handling (after implementing commands).
        5.2.5. [x] Verify `gc.collect()` is called (if it remains in the testable function).
