import time
import random
import pyautogui
from executer_base import BaseExecutor
from config import strategemTriggerKey, triggerDelayMax, triggerDelayMin

class PyAutoGuiExecuter(BaseExecutor):
    def __init__(self, model):
        super().__init__()
        self.model = model
        pyautogui.FAILSAFE = True
    
    def on_macro_triggered(self, macro):
        try:
            if macro != None:
                pyautogui.keyDown(strategemTriggerKey)
                time.sleep(0.1)
                for input in macro.commandArray:
                    pyautogui.keyDown(input)
                    time.sleep(random.uniform(triggerDelayMin,triggerDelayMax))
                    pyautogui.keyUp(input)
                    time.sleep(random.uniform(triggerDelayMin,triggerDelayMax))
                pyautogui.keyUp(strategemTriggerKey)

        except AttributeError:
            pass