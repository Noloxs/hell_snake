from pynput import keyboard

class PynputKeyparser:
    key_map = {
        "shift":keyboard.Key.shift,
        "ctrl":keyboard.Key.ctrl,
        "up":keyboard.Key.up,
        "down":keyboard.Key.down,
        "left":keyboard.Key.left,
        "right":keyboard.Key.right,
        "caps_lock":keyboard.Key.caps_lock
    }

    @classmethod
    def parse_key(cls, key):
        if key in cls.key_map:
            return cls.key_map[key]
        else:
            return key
