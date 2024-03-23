from pynput import keyboard
from pynput.keyboard import Key, Controller
import time
import random

class Strategem:
  def __init__(self, name, command):
    self.name = name
    self.command = command
  
  def call_strategem(self, keyboard_controller):
    from config import strategemTriggerKey, strategemKeys, triggerDelayMax, triggerDelayMin
    keyboard_controller.press(strategemTriggerKey)
    time.sleep(random.uniform(triggerDelayMin,triggerDelayMax))
    for input in self.command:
      keyboard_controller.press(strategemKeys[input])
      time.sleep(random.uniform(triggerDelayMin,triggerDelayMax))
      keyboard_controller.release(strategemKeys[input])
      time.sleep(random.uniform(triggerDelayMin,triggerDelayMax))
    keyboard_controller.release(strategemTriggerKey)

strategems = [
  Strategem("Resupply", [2,2,0,3]),
  Strategem("Reinforce", [0,2,3,1,0]),
  Strategem("Eagle Cluster Bomb", [0,3,2,2,3]),
  Strategem("Orbital 380 Barrage", [3,2,0,0,1,2,2]),
  Strategem("Support Autocannon", [2,1,2,0,0,3]),
  Strategem("Sentry mortar", [2,0,3,3,2]),
  Strategem("Sentry Autocannon", [2,0,3,0,1,0]),
  Strategem("Mission Hellbomb", [2,0,1,2,0,3,2,0]),
  Strategem("Eagle 500KG Bomb", [0,3,2,2,2]),
  Strategem("Support Machine Gun", [2,1,2,0,3])
  ]