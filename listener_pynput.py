from pynput import keyboard
from pynput.keyboard import Key
import time
import random

class PynputKeyListener:
    def __init__(self, model, controller):
        self.model = model
        self.listener = None
        self.controller = controller
    
    def on_press(self, key):
        try:
            macro = self.model.macros.get(key.char, None)
            if macro != None:
                self.controller.trigger_macro(macro)

        except AttributeError:
            pass
    
    def arm(self, isArmed):
        if isArmed:
            # Start the listener
            if self.listener == None:
                self.listener = keyboard.Listener(on_press=self.on_press, suppress=False)
                self.listener.start()
        else:        
            # Stop the listener
            self.listener.stop()