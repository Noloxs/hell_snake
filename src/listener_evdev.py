import threading
import select
from evdev import InputDevice, categorize, ecodes, list_devices
import constants
from src.controller import Controller
from src.key_parser_evdev import EvdevKeyparser


class EvdevKeyListener:
    """
    Wayland-compatible key listener using evdev.

    This listener reads directly from /dev/input/event* devices,
    bypassing the display server entirely. Works on Wayland, X11,
    and even in TTY.

    Requirements:
    - User must be in the 'input' group, or
    - Run with appropriate permissions (not recommended)
    - In distrobox: devices must be passed through
    """

    def __init__(self, controller: Controller):
        self.controller = controller
        self.settings = controller.get_settings_manager()

        self.getNextCallbacks = []
        self.key_press_handlers = {}
        self.key_release_handlers = {}

        self.devices = []
        self.running = False
        self.listener_thread = None

        # Find and open keyboard devices
        self._init_devices()

        # Start listening thread
        self._start_listener()

        # Attach settings change listener
        self.settings.attach_change_listener(self._on_settings_changed)
        self._on_settings_changed({'type': 'init'})

    def _init_devices(self):
        """Find and open all keyboard input devices."""
        self.devices = []

        for path in list_devices():
            try:
                device = InputDevice(path)
                capabilities = device.capabilities()

                # Check if this device has key events (EV_KEY)
                if ecodes.EV_KEY in capabilities:
                    keys = capabilities[ecodes.EV_KEY]
                    # Check if it has typical keyboard keys (letters/numbers)
                    has_keyboard_keys = any(
                        ecodes.KEY_A <= k <= ecodes.KEY_Z or
                        ecodes.KEY_1 <= k <= ecodes.KEY_0
                        for k in keys
                    )
                    if has_keyboard_keys:
                        self.devices.append(device)
                        print(f"[evdev] Listening on: {device.name} ({device.path})")
            except (PermissionError, OSError) as e:
                print(f"[evdev] Cannot access {path}: {e}")

        if not self.devices:
            print("[evdev] WARNING: No keyboard devices found!")
            print("[evdev] Make sure you have read access to /dev/input/event* devices.")
            print("[evdev] Try: sudo usermod -aG input $USER (then log out and back in)")

    def _start_listener(self):
        """Start the background thread that reads key events."""
        self.running = True
        self.listener_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listener_thread.start()

    def _listen_loop(self):
        """Main event loop - runs in background thread."""
        while self.running and self.devices:
            # Use select to wait for events on any device
            r, _, _ = select.select(self.devices, [], [], 0.1)

            for device in r:
                try:
                    for event in device.read():
                        if event.type == ecodes.EV_KEY:
                            # event.value: 0 = release, 1 = press, 2 = repeat
                            if event.value == 1:  # Key press
                                self._handle_key_press(event.code)
                            elif event.value == 0:  # Key release
                                self._handle_key_release(event.code)
                except OSError:
                    # Device disconnected
                    self.devices.remove(device)

    def _handle_key_press(self, code):
        """Handle a key press event."""
        # Handle "get next key" callbacks first
        if self.getNextCallbacks:
            strKey = EvdevKeyparser.code_to_string(code)
            if strKey:
                for callback in self.getNextCallbacks:
                    callback(strKey)
                self.getNextCallbacks.clear()
                return

        # Convert code to our internal representation
        entry = self._parse_key(code)

        # Call registered press handlers
        if entry in self.key_press_handlers:
            self.key_press_handlers[entry](entry)

        # Check for macro triggers when armed
        if self.controller.is_armed():
            # For character keys, also try the string representation
            char_entry = EvdevKeyparser.code_to_string(code)
            macro = self.controller.getMacroForKey(entry)
            if macro is None and char_entry:
                macro = self.controller.getMacroForKey(char_entry)
            if macro is not None:
                self.controller.trigger_macro(macro)

    def _handle_key_release(self, code):
        """Handle a key release event."""
        entry = self._parse_key(code)

        if entry in self.key_release_handlers:
            self.key_release_handlers[entry](entry)

    def _parse_key(self, code):
        """Convert evdev code to internal key representation."""
        return code

    ### Handlers ###

    def handle_global_arm_press(self, key):
        if self.settings.globalArmMode == constants.ARM_MODE_TOGGLE:
            self.controller.toggle_armed()
        elif self.settings.globalArmMode == constants.ARM_MODE_PUSH and not self.controller.is_armed():
            self.controller.set_armed(True)

    def handle_global_arm_release(self, key):
        if self.settings.globalArmMode == constants.ARM_MODE_PUSH:
            self.controller.set_armed(False)

    def handle_next_loadout(self, key):
        if not self.controller.is_armed():
            self.controller.cycle_loadout(+1)

    def handle_prev_loadout(self, key):
        if not self.controller.is_armed():
            self.controller.cycle_loadout(-1)

    ### Settings ###

    def _on_settings_changed(self, event):
        """Called when settings are updated."""
        if event['type'] == 'setattr' or event['type'] == 'init':
            self.globalArmKey = EvdevKeyparser.parse_key(self.settings.globalArmKey)
            self.nextLoadoutKey = EvdevKeyparser.parse_key(self.settings.nextLoadoutKey)
            self.prevLoadoutKey = EvdevKeyparser.parse_key(self.settings.prevLoadoutKey)

            self.key_press_handlers = {}
            self.key_release_handlers = {}

            if self.globalArmKey is not None:
                self.key_press_handlers[self.globalArmKey] = self.handle_global_arm_press
                self.key_release_handlers[self.globalArmKey] = self.handle_global_arm_release
            if self.nextLoadoutKey is not None:
                self.key_press_handlers[self.nextLoadoutKey] = self.handle_next_loadout
            if self.prevLoadoutKey is not None:
                self.key_press_handlers[self.prevLoadoutKey] = self.handle_prev_loadout

    ### Public API ###

    def get_next_key(self, callback):
        """Register a callback to receive the next key press."""
        self.getNextCallbacks.append(callback)

    def stop(self):
        """Stop the listener and clean up."""
        self.running = False
        if self.listener_thread:
            self.listener_thread.join(timeout=1.0)
        for device in self.devices:
            try:
                device.close()
            except Exception:
                pass
        self.devices = []
