from pynput import keyboard
from pynput.keyboard import Controller
import time
import random
from executer_base import BaseExecutor
from config import strategemTriggerKey, triggerDelayMax, triggerDelayMin

class PynputExecuter(BaseExecutor):
    def __init__(self, model):
        super().__init__()
        self.model = model
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