from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyautogui
import time
import random
from config import strategemTriggerKey, triggerDelayMax, triggerDelayMin, pyautoguiTriggerKey, selectedKeyboardEmulator

class MacroExecuter:
    def __init__(self, model):
        self.model = model
        self.listener = None
        self.keyboard_controller = Controller()
    
    def on_press_pynput(self, key):
        try:
            macro = self.model.macros.get(key.char, None)
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
    
    def on_press_pyautogui(self, key):
        try:
            macro = self.model.macros.get(key.char, None)
            if macro != None:
                with pyautogui.hold(pyautoguiTriggerKey):
                    pyautogui.press(macro.commandArray)
                    time.sleep(random.uniform(triggerDelayMin,triggerDelayMax))

        except AttributeError:
            pass

    def arm(self, isArmed):
        if isArmed:
            # Start the listener
            if self.listener == None:
                if selectedKeyboardEmulator == 'pyautogui':
                    self.listener = keyboard.Listener(on_press=self.on_press_pyautogui, suppress=False)
                elif selectedKeyboardEmulator == 'pynput':
                    self.listener = keyboard.Listener(on_press=self.on_press_pynput, suppress=False)
                else:
                    self.listener = keyboard.Listener(on_press=self.on_press_pynput, suppress=False)

                self.listener.start()
        else:        
            # Stop the listener
            self.listener.stop()