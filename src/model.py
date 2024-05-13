from src.strategem import Strategem
import json
from src import utilities, constants
from src.classes.settings import Settings,Loadout

class Model:
    def __init__(self):
        self.isArmed = False

        with open(constants.RESOURCE_PATH+"strategems.json") as json_file:
            tmp = json.load(json_file)
        
        self.strategems = {}
        for index, item in tmp.items():
            name = item["name"]
            strate = Strategem(**item)
            self.strategems.update({index: strate})
        
        self.settings = Settings.getInstance()
        self.settings.loadFromFile()

    def update_macro_binding(self, key, strategemId):
        strategem = self.strategems[strategemId]
        self.currentLoadout.macroKeys[key] = strategemId
        self.macros.update({key:strategem})
    
    def add_loadout(self, loadoutName):
        self.settings.loadouts.update({utilities.generateUuid(): Loadout(loadoutName, {"1":"1"})})

    def delete_loadout(self, loadoutId):
        self.settings.loadouts.pop(loadoutId)
    
    def get_next_loadout(self):
        if len(self.settings.loadouts) > 0:
            return next(iter(self.settings.loadouts.keys()))
        return None

    def update_loadout(self, id, loadout):
        self.settings.loadouts[id] = loadout

    def set_active_loadout(self, id):
        self.currentLoadoutId = id
        self.macros = {}
        if id == None:
            self.currentLoadout = None
            self.macroKeys = None
        else:
            self.currentLoadout = self.settings.loadouts[id]
            self.macroKeys = self.currentLoadout.macroKeys
            for key, strategemId in self.macroKeys.items():
                self.macros.update({key:self.strategems[strategemId]})      

    def set_armed(self, isArmed):
        self.isArmed = isArmed
