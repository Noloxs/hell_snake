from pynput import keyboard
from strategem import strategems

strategemTriggerKey=keyboard.Key.ctrl
strategemKeys = ["i", "j", "k", "l"]

triggerDelayMin = 0.05
triggerDelayMax = 0.075

macroKeys = {
    "1": strategems[1],
    "2": strategems[2],
    "3": strategems[8],
    "4": strategems[5],
    "5": strategems[6],
    "6": strategems[7],
    "7": strategems[9],
    "8": strategems[4],
    "9": strategems[0]
}