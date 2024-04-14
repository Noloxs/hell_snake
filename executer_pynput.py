from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyautogui
import time
import random
from config import strategemTriggerKey, triggerDelayMax, triggerDelayMin

class PynputExecuter:
    def __init__(self, model):
        self.model = model
        self.listener = None
        self.keyboard_controller = Controller()
    
    def on_macro_triggered(self, macro):
        try:
            if macro != None:
                self.keyboard_controller.press(strategemTriggerKey)
                time.sleep(0.1)
                for input in macro.commandArray:
                    self.keyboard_controller.press(input)
                    time.sleep(random.uniform(triggerDelayMin,triggerDelayMax))
                    self.keyboard_controller.release(input)
                    time.sleep(random.uniform(triggerDelayMin,triggerDelayMax))
                self.keyboard_controller.release(strategemTriggerKey)

        except AttributeError:
            pass
