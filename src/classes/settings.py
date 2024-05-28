# This module defines the Settings class which provides a singleton instance to manage application settings,
# allowing settings to be loaded from a file, updated dynamically, and used across the application.
# The Settings class follows a singleton pattern.

import json
from src import utilities, constants

class Settings:
    _instance = None  # Class variable to hold the singleton instance

    @classmethod
    def getInstance(cls):
        """
        Method to retrieve or create a singleton instance of the Settings class.

        This method checks if an instance of the class has already been created (stored in `_instance`).
        If not, it creates a new instance and stores it in `_instance`. It then returns this singleton instance.

        Returns:
            Settings: a singleton instance of the Settings class.
        """
        if cls._instance is None:
            cls._instance = cls()  # Create a new instance if one doesn't exist
        return cls._instance

    def __init__(self):
        # Load defaults, protecting against missing values
        self.loadDefaults()
        # Load settings from file, overriding defaults as needed
        self.loadFromFile()
        ## Consider no version to be version 1
        if not hasattr(self, "version") or self.version < 2:
            self.migrate_1_to_2()
        ## For future use:
        # if self.version == 2:
        #     self.migrate_2_to_3()
        print("Settings initialized")

    def loadDefaults(self):
        """
        We load a base set of settings, in case the user has no settings file.
        """
        self.loadouts = {utilities.generateUuid(): Loadout("Loadout 1", {"1": "1"})}
        self.triggerKey = "ctrl"
        self.triggerDelay = 100
        self.triggerDelayJitter = 30
        self.stratagemKeys = ["w", "a", "s", "d"]
        self.stratagemKeyDelay = 30
        self.stratagemKeyDelayJitter = 20
        self.selectedExecutor = constants.EXECUTOR_PYNPUT
        self.globalArmKey = None
        self.globalArmMode = constants.ARM_MODE_TOGGLE
        self.view_framework = constants.VIEW_PYQT5

    def loadFromFile(self):
        try:
            with open(constants.SETTINGS_PATH) as json_file:
                data = json.load(json_file)
                if 'loadouts' in data:
                    self.parseLoadouts(data['loadouts'])
                self.parseSettings(data)
            return True
        except (OSError, json.JSONDecodeError):
            return False

    def parseLoadouts(self, loadout_data):
        # We expect the root loadouts element
        loadouts = {}
        for id, item in loadout_data.items():
            loadout = Loadout(item['name'], item['macroKeys'])
            loadouts[id] = loadout
        self.loadouts = loadouts

    def parseSettings(self, settings_data):
        for attribute, value in settings_data.items():
            # Exclude 'loadouts' from this general assignment because it's already processed
            if attribute != 'loadouts':
                setattr(self, attribute, value)


    def saveToFile(self):
        with open(constants.SETTINGS_PATH, "w") as file:
            settings_as_json = json.dumps(self, default=vars, indent=2)
            file.write(settings_as_json)

    def migrate_1_to_2(self):
        self.version = 2
        if hasattr(self, "strategemKeys"):
            self.stratagemKeys = self.strategemKeys
            del self.strategemKeys
        if hasattr(self, "strategemKeyDelay"):
            self.stratagemKeyDelay = self.strategemKeyDelay
            del self.strategemKeyDelay
        if hasattr(self, "strategemKeyDelayJitter"):
            self.stratagemKeyDelayJitter = self.strategemKeyDelayJitter
            del self.strategemKeyDelayJitter
        print("Settings migrated to version 2. Remember to save.")


class Loadout:
    """
    Simple data class designed to handle the storage and management of different 
    configurations of macro keys for a particular setup.
    This class is used primarily in the settings.
    """
    def __init__(self, name, macroKeys):
        self.name = name
        self.macroKeys = macroKeys