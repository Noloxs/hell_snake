from pynput import keyboard

def parse_key(key):
    if(key == "shift"): return keyboard.Key.shift
    elif(key == "ctrl"): return keyboard.Key.ctrl
    elif(key == "up"): return keyboard.Key.up
    elif(key == "down"): return keyboard.Key.down
    elif(key == "left"): return keyboard.Key.left
    elif(key == "right"): return keyboard.Key.right
    elif(key == "caps_lock"): return keyboard.Key.caps_lock
    else: return key