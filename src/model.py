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

        self.current_loadout_id = settingsManager.currentLoadoutId

        # Handle armed state
        self.is_armed = False

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

    def get_current_loadout_macros(self):
        current_loadout = self.loadoutsManager.loadouts.get(self.settingsManager.currentLoadoutId, None)
        macros = {key: self._stratagems[stratagemId] for key, stratagemId in current_loadout.macroKeys.items()}
        return macros

    def update_macro_binding(self, key, stratagemId):
        current_loadout = self.loadoutsManager.loadouts.get(self.settingsManager.currentLoadoutId, None)
        current_loadout.macroKeys[key] = stratagemId

    def set_active_loadout(self, id):
        self.current_loadout_id = id

    def set_armed(self, is_armed):
        self.is_armed = is_armed
