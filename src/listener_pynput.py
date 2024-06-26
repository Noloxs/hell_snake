from pynput import keyboard
import constants
from src.controller import Controller
from src.key_parser_pynput import PynputKeyparser

class PynputKeyListener:
    def __init__(self, controller : Controller):
        self.controller = controller
        self.settings = controller.get_settings_manager()
        self.getNextCallbacks = []

        # Initialize the actual keyboard event listener
        self.listener = None
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release, suppress=False)
        self.listener.start()

        # Attach a listener to notify us of changes to settings
        self.settings.attach_change_listener(self._on_settings_changed)
        self._on_settings_changed({'type': 'init'})
        
    ### Handlers ###

    # Global arm handler
    def handle_global_arm_press(self, key):
        if (self.settings.globalArmMode == constants.ARM_MODE_TOGGLE):
            self.controller.toggle_armed()
        elif (self.settings.globalArmMode == constants.ARM_MODE_PUSH and not self.controller.is_armed()):
            self.controller.set_armed(True)
    def handle_global_arm_release(self, key):
        if (self.settings.globalArmMode == constants.ARM_MODE_PUSH):
            self.controller.set_armed(False)

    # Loadout browser
    def handle_next_loadout(self, key):
        if(not self.controller.is_armed()):
            self.controller.cycle_loadout(+1)
    def handle_prev_loadout(self, key):
        if(not self.controller.is_armed()):
            self.controller.cycle_loadout(-1)

    ### Helpers ###
    def _on_settings_changed(self, event):
        ''' This function is called when settings are updated, since we attach it as a listener in __init__ '''
        if event['type']=='setattr':
            self.globalArmKey = PynputKeyparser.parse_key(self.settings.globalArmKey)
            self.nextLoadoutKey = PynputKeyparser.parse_key(self.settings.nextLoadoutKey)
            self.prevLoadoutKey = PynputKeyparser.parse_key(self.settings.prevLoadoutKey)
            self.key_press_handlers = {
                self.globalArmKey: self.handle_global_arm_press,
                self.nextLoadoutKey: self.handle_next_loadout,
                self.prevLoadoutKey: self.handle_prev_loadout,
            }
            self.key_release_handlers = {
                self.globalArmKey: self.handle_global_arm_release
            }


    def on_press(self, key):
        if len(self.getNextCallbacks) > 0:
            strKey = self.parse_key_to_string(key)
            for callback in self.getNextCallbacks:
                callback(strKey)
            self.getNextCallbacks.clear()
        
        if (key is None):
            return

        entry = self.parse_key(key)

        # Call key handler
        if entry in self.key_press_handlers:
            self.key_press_handlers[entry](key)

        if(self.controller.is_armed()):
            macro = self.controller.getMacroForKey(entry)
            if macro is not None:
                self.controller.trigger_macro(macro)
    
    def on_release(self, key):
        if (key is None):
            return
        entry = self.parse_key(key)

        # Call key handler
        if entry in self.key_release_handlers:
            self.key_release_handlers[entry](key)

    def parse_key(self, key):
        if isinstance(key, keyboard.Key):
            return key
        elif isinstance(key, keyboard.KeyCode):
            return key.char
    
    def parse_key_to_string(self, key):
        if isinstance(key, keyboard.Key):
            return key.name
        elif isinstance(key, keyboard.KeyCode):
            return key.char

    def get_next_key(self, callback):
        self.getNextCallbacks.append(callback)