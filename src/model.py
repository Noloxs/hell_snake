import constants
from src.loadouts import LoadoutManager
from src.settings import SettingsManager
import json
from src.stratagem import Stratagem

class Model:
    def __init__(self, loadoutsManager: LoadoutManager, settingsManager: SettingsManager):
        self.loadoutsManager = loadoutsManager
        self.settingsManager = settingsManager

        # Ensure current loadout is valid
        if not hasattr(self.settingsManager, "currentLoadoutId") \
          or self.settingsManager.currentLoadoutId not in self.loadoutsManager.loadouts:
            self.settingsManager.currentLoadoutId = next(iter(self.loadoutsManager.loadouts))

        self.currentLoadoutId = settingsManager.currentLoadoutId

        # Handle armed state
        self.isArmed = False

        # List of stratagems, and the respective macro definition
        self._stratagems = self.loadStratagemsFromFile()

    def loadStratagemsFromFile(self):
        with open(constants.RESOURCE_PATH+"stratagems.json") as json_file:
            tmp = json.load(json_file)
        
        stratagems = {}
        for index, item in tmp.items():
            stratagem = Stratagem(**item)
            stratagems.update({index: stratagem})

        return stratagems

    def update_macro_binding(self, key, stratagemId):
        stratagem = self._stratagems[stratagemId]
        self.currentLoadout.macroKeys[key] = stratagemId
        self.macros.update({key:stratagem})

    def set_active_loadout(self, id):
        self.currentLoadoutId = id
        self.macros = {}
        if id is None:
            self.currentLoadout = None
            self.macroKeys = None
        else:
            self.currentLoadout = self.loadoutsManager.loadouts.get(id)
            self.macroKeys = self.currentLoadout.macroKeys
            for key, stratagemId in self.macroKeys.items():
                self.macros.update({key:self._stratagems[stratagemId]})      

    def set_armed(self, isArmed):
        self.isArmed = isArmed
