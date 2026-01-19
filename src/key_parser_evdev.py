from evdev import ecodes

class EvdevKeyparser:
    """Maps string key names to evdev key codes."""

    key_map = {
        "shift": ecodes.KEY_LEFTSHIFT,
        "ctrl": ecodes.KEY_LEFTCTRL,
        "up": ecodes.KEY_UP,
        "down": ecodes.KEY_DOWN,
        "left": ecodes.KEY_LEFT,
        "right": ecodes.KEY_RIGHT,
        "caps_lock": ecodes.KEY_CAPSLOCK,
        "alt": ecodes.KEY_LEFTALT,
        "tab": ecodes.KEY_TAB,
        "enter": ecodes.KEY_ENTER,
        "space": ecodes.KEY_SPACE,
        "backspace": ecodes.KEY_BACKSPACE,
        "escape": ecodes.KEY_ESC,
        "esc": ecodes.KEY_ESC,
    }

    # Reverse map: evdev code -> string name
    code_to_name = {v: k for k, v in key_map.items()}

    # Map single characters to their evdev codes
    char_to_code = {
        'a': ecodes.KEY_A, 'b': ecodes.KEY_B, 'c': ecodes.KEY_C, 'd': ecodes.KEY_D,
        'e': ecodes.KEY_E, 'f': ecodes.KEY_F, 'g': ecodes.KEY_G, 'h': ecodes.KEY_H,
        'i': ecodes.KEY_I, 'j': ecodes.KEY_J, 'k': ecodes.KEY_K, 'l': ecodes.KEY_L,
        'm': ecodes.KEY_M, 'n': ecodes.KEY_N, 'o': ecodes.KEY_O, 'p': ecodes.KEY_P,
        'q': ecodes.KEY_Q, 'r': ecodes.KEY_R, 's': ecodes.KEY_S, 't': ecodes.KEY_T,
        'u': ecodes.KEY_U, 'v': ecodes.KEY_V, 'w': ecodes.KEY_W, 'x': ecodes.KEY_X,
        'y': ecodes.KEY_Y, 'z': ecodes.KEY_Z,
        '1': ecodes.KEY_1, '2': ecodes.KEY_2, '3': ecodes.KEY_3, '4': ecodes.KEY_4,
        '5': ecodes.KEY_5, '6': ecodes.KEY_6, '7': ecodes.KEY_7, '8': ecodes.KEY_8,
        '9': ecodes.KEY_9, '0': ecodes.KEY_0,
    }

    # Reverse map: evdev code -> character
    code_to_char = {v: k for k, v in char_to_code.items()}

    @classmethod
    def parse_key(cls, key):
        """Convert a string key name to an evdev key code."""
        if key is None:
            return None
        if key in cls.key_map:
            return cls.key_map[key]
        elif key in cls.char_to_code:
            return cls.char_to_code[key]
        elif isinstance(key, int):
            return key
        else:
            # Try to find it in ecodes directly
            key_attr = f"KEY_{key.upper()}"
            if hasattr(ecodes, key_attr):
                return getattr(ecodes, key_attr)
            return None

    @classmethod
    def code_to_string(cls, code):
        """Convert an evdev key code back to a string representation."""
        if code in cls.code_to_name:
            return cls.code_to_name[code]
        elif code in cls.code_to_char:
            return cls.code_to_char[code]
        else:
            # Try to find the name in ecodes
            for name, val in ecodes.KEY.items():
                if val == code:
                    return name.lower().replace('key_', '')
            return None
