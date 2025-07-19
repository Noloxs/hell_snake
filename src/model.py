from typing import Dict
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
        if not hasattr(self.settingsManager, "currentLoadoutId")           or self.settingsManager.currentLoadoutId not in self.loadoutsManager.loadouts:
            self.settingsManager.currentLoadoutId = next(iter(self.loadoutsManager.loadouts))

        # Handle armed state
        self.is_armed = False

        # List of stratagems, and the respective macro definition
        self._stratagems: Dict[Stratagem] = {}
        self._loadStratagemsFromFile()

    def _loadStratagemsFromFile(self):
        """Load stratagems from a JSON file and return a dictionary of Stratagem objects."""
        with open(constants.RESOURCE_PATH+"stratagems.json") as json_file:
            tmp = json.load(json_file)
        
        self._stratagems = {}
        for index, item in tmp.items():
            stratagem = Stratagem(**item)
            self._stratagems.update({index: stratagem})

    def prepare_stratagems(self, controller):
        """Prepare stratagems for use in selected executer."""
        for stratagem in self._stratagems.values():
            stratagem.prepare(controller)

    def get_current_loadout_macros(self):
        """Return a dictionary of macro definitions for the current loadout."""
        current_loadout = self.loadoutsManager.loadouts.get(self.settingsManager.currentLoadoutId, None)
        macros = {key: self._stratagems[stratagemId] for key, stratagemId in current_loadout.macroKeys.items()}
        return macros

    def update_macro_binding(self, key, stratagemId):
        """Update the macro binding for the current loadout."""
        current_loadout = self.loadoutsManager.loadouts.get(self.settingsManager.currentLoadoutId, None)
        current_loadout.macroKeys[key] = stratagemId

    def set_armed(self, is_armed):
        """Set the armed state."""
        self.is_armed = is_armed


    def get_stratagem_by_id(self, stratagemId):
        """Return a stratagem by its ID."""
        return self._stratagems.get(stratagemId)

    def get_all_stratagems(self):
        """Return all stratagems."""
        return self._stratagems

    def get_all_loadouts(self):
        """Return all loadouts."""
        return self.loadoutsManager.loadouts

    def get_loadout_by_id(self, loadoutId):
        """Return a loadout by its ID."""
        return self.loadoutsManager.loadouts.get(loadoutId)

    def get_current_loadout(self):
        """Return the current loadout."""
        return self.loadoutsManager.loadouts.get(self.settingsManager.currentLoadoutId)

    def get_current_loadout_id(self):
        """Return the current loadout ID."""
        return self.settingsManager.currentLoadoutId

    def set_current_loadout_id(self, loadoutId):
        """Set the current loadout ID."""
        self.settingsManager.currentLoadoutId = loadoutId

    def add_loadout(self, loadoutName):
        """Add a new loadout."""
        return self.loadoutsManager.addLoadout(loadoutName)

    def delete_loadout(self, loadoutId):
        """Delete a loadout."""
        self.loadoutsManager.deleteLoadout(loadoutId)

    def update_loadout(self, loadoutId, loadout):
        """Update a loadout."""
        self.loadoutsManager.updateLoadout(loadoutId, loadout)

    def save_loadouts(self):
        """Save loadouts to file."""
        self.loadoutsManager.saveToFile()

    def export_all_loadouts(self, filePath):
        """Export all loadouts to file."""
        self.loadoutsManager.exportLoadoutsToJson(filePath)

    def import_all_loadouts(self, filePath):
        """Import all loadouts from file."""
        self.loadoutsManager.importLoadoutsFromJson(filePath)

    def load_loadouts(self):
        """Load loadouts from file."""
        self.loadoutsManager.loadFromFile()
