from pynput import keyboard
from src import key_parser_pynput, constants

class PynputKeyListener:
    def __init__(self, model, controller):
        self.model = model
        self.globalArmKey = key_parser_pynput.parse_key(self.model.settings.globalArmKey)
        self.listener = None
        self.controller = controller
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release, suppress=False)
        self.listener.start()
        self.getNextCallbacks = []
        self.key_press_handlers = {
            self.globalArmKey: self.handle_global_arm_press,
            # TODO: Put these keys in settings
            "+": self.handle_next_loadout,
            "-": self.handle_prev_loadout,
        }
        self.key_release_handlers = {
            self.globalArmKey: self.handle_global_arm_release
        }
    

    ### Handlers ###

    # Global arm handler
    def handle_global_arm_press(self, key):
        if (self.model.settings.globalArmMode == constants.ARM_MODE_TOGGLE):
            self.controller.toggle_armed()
        elif (self.model.settings.globalArmMode == constants.ARM_MODE_PUSH and not self.model.isArmed):
            self.controller.set_armed(True)
    def handle_global_arm_release(self, key):
        if (self.model.settings.globalArmMode == constants.ARM_MODE_PUSH):
            self.controller.set_armed(False)

    # Loadout browser
    def handle_next_loadout(self, key):
        self.controller.cycle_next_loadout()
    def handle_prev_loadout(self, key):
        self.controller.cycle_prev_loadout()

    ### Helpers ###
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
            macro = self.model.macros.get(entry, None)
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