from pynput import keyboard
import constants
from src.key_parser_pynput import PynputKeyparser
from src.model import Model

class PynputKeyListener:
    def __init__(self, model : Model, controller):
        self.model = model
        self.controller = controller
        self.getNextCallbacks = []

        # Initialize the actual keyboard event listener
        self.listener = None
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release, suppress=False)
        self.listener.start()

        # Attach a listener to notify us of changes to settings
        self.model.settingsManager.attach_change_listener(self._on_settings_changed)
        self._on_settings_changed()
        
    ### Handlers ###

    # Global arm handler
    def handle_global_arm_press(self, key):
        if (self.model.settingsManager.globalArmMode == constants.ARM_MODE_TOGGLE):
            self.controller.toggle_armed()
        elif (self.model.settingsManager.globalArmMode == constants.ARM_MODE_PUSH and not self.model.isArmed):
            self.controller.set_armed(True)
    def handle_global_arm_release(self, key):
        if (self.model.settingsManager.globalArmMode == constants.ARM_MODE_PUSH):
            self.controller.set_armed(False)

    # Loadout browser
    def handle_next_loadout(self, key):
        if(not self.model.isArmed):
            self.controller.cycle_loadout(+1)
    def handle_prev_loadout(self, key):
        if(not self.model.isArmed):
            self.controller.cycle_loadout(-1)

    ### Helpers ###
    def _on_settings_changed(self):
        ''' This function is called when settings are updated, since we attach it as a listener in __init__ '''
        self.globalArmKey = PynputKeyparser.parse_key(self.model.settingsManager.globalArmKey)
        self.nextLoadoutKey = PynputKeyparser.parse_key(self.model.settingsManager.nextLoadoutKey)
        self.prevLoadoutKey = PynputKeyparser.parse_key(self.model.settingsManager.prevLoadoutKey)
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

        if(self.model.isArmed):
            macro = self.model.getMacroForKey(entry)
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