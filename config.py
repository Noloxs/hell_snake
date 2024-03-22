from pynput import keyboard
from strategem import strategems

strategemTriggerKey=keyboard.Key.ctrl
strategemKeys = ["i", "j", "k", "l"]

macroKeys = {
    "1": strategems[1],
    "2": strategems[2],
    "3": strategems[3],
    "4": strategems[5],
    "5": strategems[6],
    "6": strategems[7],
    "8": strategems[4],
    "9": strategems[0]
}