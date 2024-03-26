from pynput import keyboard
from pynput.keyboard import Key, Controller
from config import macroKeys

# Create a keyboard controller
keyboard_controller = Controller()
listener = None

# Function to execute key events when "1" is pressed
def on_press(key):
    try:
        macro = macroKeys.get(key.char, None)
        if macro != None:
            macro.call_strategem(keyboard_controller)

    except AttributeError:
        pass

def on_release(key):
    print(key)

def arm(isArmed):
    if isArmed:
        print("Starting listener")
        # Start the listener
        global listener

        if listener == None:  
            listener = keyboard.Listener(on_press=on_press,suppress=True)
            listener.start()
    else:
        # Stop the listener
        print("Stopping listener")
        listener.stop()