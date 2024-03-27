from pynput import keyboard
from pynput.keyboard import Key, Controller
from model import Model

# Create a keyboard controller
keyboard_controller = Controller()
model = Model()

# Function to execute key events when "1" is pressed
def on_press(key):
    try:
        macro = model.macros.get(key.char, None)
        if macro != None:
            macro.call_strategem(keyboard_controller)

    except AttributeError:
        pass

# Print active macros
print("----- ACTIVE MACROS -----")
print("-------------------------")
for key, macro in model.macros.items():
    print(key, ": ", macro.name)
print("-------------------------")

# Start the listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()