import constants
from src.loadouts import LoadoutManager,Loadout
import utilities
import json
from src.stratagem import Stratagem

class Model:
    def __init__(self):
        self.isArmed = False

        # List of stratagems, and the respective macro definition
        self.stratagems = self.loadStratagemsFromFile()

        # Loadout manager handles persistance of loadouts.
        self.loadoutManager = LoadoutManager()
        # a Loadout is a list of keys, and the respective stratagem to be activated
        # self.set_active_loadout(self.loadoutManager.getCurrentLoadout())

    def loadStratagemsFromFile(self):
        with open(constants.RESOURCE_PATH+"stratagems.json") as json_file:
            tmp = json.load(json_file)
        
        stratagems = {}
        for index, item in tmp.items():
            stratagem = Stratagem(**item)
            stratagems.update({index: stratagem})

        return stratagems

    def update_macro_binding(self, key, stratagemId):
        stratagem = self.stratagems[stratagemId]
        self.currentLoadout.macroKeys[key] = stratagemId
        self.macros.update({key:stratagem})

    def getMacroForKey(self, key):
        return self.macros[key]

    # def get_next_loadout(self):
    #     return self.loadoutManager.getCurrentLoadout()

    def set_active_loadout(self, id):
        self.currentLoadoutId = id
        self.macros = {}
        if id is None:
            self.currentLoadout = None
            self.macroKeys = None
        else:
            self.currentLoadout = self.loadoutManager.loadouts[id]
            self.macroKeys = self.currentLoadout.macroKeys
            for key, stratagemId in self.macroKeys.items():
                self.macros.update({key:self.stratagems[stratagemId]})      

    def set_armed(self, isArmed):
        self.isArmed = isArmed
