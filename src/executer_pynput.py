from pynput.keyboard import Controller
from src.executer_base import BaseExecutor
from src import utilities, key_parser_pynput
import threading

class PynputExecuter(BaseExecutor):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.keyboard_controller = Controller()
        self.triggerKey = self.parse_macro_key(self.model.settings.triggerKey)
    
    def on_macro_triggered(self, macro):
        try:
            if macro != None:
                t1 = threading.Thread(target=self.execute_macro, args=(macro,))
                t1.start()

        except AttributeError:
            pass
    
    def execute_macro(self, macro):
        self.keyboard_controller.press(self.triggerKey)
        utilities.sleepTriggerKey(self.model)
        for input in macro.commandArray:
            self.keyboard_controller.press(input)
            utilities.sleepStrategemKey(self.model)
            self.keyboard_controller.release(input)
            utilities.sleepStrategemKey(self.model)
        self.keyboard_controller.release(self.triggerKey)

    def parse_macro_key(self, key):
        return key_parser_pynput.parse_key(key)