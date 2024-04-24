from pynput import keyboard
from pynput.keyboard import Controller
from executer_base import BaseExecutor
import utilities

class PynputExecuter(BaseExecutor):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.keyboard_controller = Controller()
        self.triggerKey = self.parse_macro_key(self.model.settings.triggerKey)
    
    def on_macro_triggered(self, macro):
        try:
            if macro != None:
                self.keyboard_controller.press(self.triggerKey)
                utilities.sleepTriggerKey(self.model)
                for input in macro.commandArray:
                    self.keyboard_controller.press(input)
                    utilities.sleepStrategemKey(self.model)
                    self.keyboard_controller.release(input)
                    utilities.sleepStrategemKey(self.model)
                self.keyboard_controller.release(self.triggerKey)

        except AttributeError:
            pass
    
    def parse_macro_key(self, key):
        if(key == "shift"): return keyboard.Key.shift
        elif(key == "ctrl"): return keyboard.Key.ctrl
        elif(key == "up"): return keyboard.Key.up
        elif(key == "down"): return keyboard.Key.down
        elif(key == "left"): return keyboard.Key.left
        elif(key == "right"): return keyboard.Key.right
        else: return key