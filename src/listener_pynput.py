from pynput import keyboard
from pynput.keyboard import Key
import time
import random
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
    
    def on_press(self, key):
        if len(self.getNextCallbacks) > 0:
            strKey = self.parse_key_to_string(key)
            for callback in self.getNextCallbacks:
                callback(strKey)
            self.getNextCallbacks.clear()
        
        if (key == None):
            return

        entry = self.parse_key(key)
        if(self.globalArmKey != None and self.globalArmKey == entry):
            if (self.model.settings.globalArmMode == constants.ARM_MODE_TOGGLE):
                self.controller.toggle_armed()
            elif (self.model.settings.globalArmMode == constants.ARM_MODE_PUSH and not self.model.isArmed):
                self.controller.set_armed(True)
            return

        if(self.model.isArmed):
            macro = self.model.macros.get(entry, None)
            if macro != None:
                self.controller.trigger_macro(macro)
    
    def on_release(self, key):
        if (self.model.settings.globalArmMode == constants.ARM_MODE_PUSH):
            if (key == None):
                return

            entry = self.parse_key(key)
            if(self.globalArmKey != None and self.globalArmKey == entry):
                self.controller.set_armed(False)
                return

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