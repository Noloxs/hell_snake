from src.executer_base import BaseExecutor
import subprocess
from src import utilities

class XdotoolExecuter(BaseExecutor):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.isExecuting = False
        self.triggerKey = self.parse_macro_key(self.model.settings.triggerKey)
    
    def on_macro_triggered(self, macro):
        if self.isExecuting:
            print("Ignore, executing")
            return
        if macro != None:
            self.isExecuting = True
            subprocess.call(["xdotool", "keydown", self.triggerKey])
        utilities.sleepTriggerKey(self.model)
        for input in macro.commandArray:
            subprocess.call(["xdotool", "keydown", input])
            utilities.sleepStrategemKey(self.model)
            subprocess.call(["xdotool", "keyup", input])
            utilities.sleepStrategemKey(self.model)
        subprocess.call(["xdotool", "keyup", self.triggerKey])
        self.isExecuting = False

    def parse_macro_key(self, key):
        if(key == "shift"): return "Shift"
        elif(key == "ctrl"): return "Ctrl"
        elif(key == "up"): return "Up"
        elif(key == "down"): return "Down"
        elif(key == "left"): return "Left"
        elif(key == "right"): return "Right"
        elif(key == "caps_lock"): return "Caps_Lock"
        else: return key