from pynput import keyboard

def parse_key(key):
    if key in key_map:
        return key_map[key]
    else:
        return key

key_map = {
    "shift":keyboard.Key.shift,
    "ctrl":keyboard.Key.ctrl,
    "up":keyboard.Key.up,
    "down":keyboard.Key.down,
    "left":keyboard.Key.left,
    "right":keyboard.Key.right,
    "caps_lock":keyboard.Key.caps_lock
    } 