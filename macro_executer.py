from pynput import keyboard
from pynput.keyboard import Key, Controller

class MacroExecuter:
    def __init__(self, model):
        self.model = model
        self.listener = None
        self.keyboard_controller = Controller()

    # Function to execute key events when "1" is pressed
    def on_press(self, key):
        try:
            macro = self.model.macros.get(key.char, None)
            if macro != None:
                macro.call_strategem(self.keyboard_controller)

        except AttributeError:
            pass

    def on_release(self, key):
        print(key)

    def arm(self, isArmed):
        if isArmed:
            # Start the listener
            if self.listener == None:  
                self.listener = keyboard.Listener(on_press=self.on_press, suppress=False)
                self.listener.start()
        else:        
            # Stop the listener
            self.listener.stop()