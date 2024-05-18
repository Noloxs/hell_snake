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
        self.loadFromFile()
        print("Settings initialized")

    def __getattr__(self, name):
        print("Requested unknown value for for %s"%(name))
        return "unknown"

    def loadFromFile(self):
        try:
            with open(constants.SETTINGS_PATH) as json_file:
                data = json.load(json_file)
                for attribute, value in data.items():
                    setattr(self, attribute, value)
                    if attribute == "loadouts":
                        loadouts = {}
                        for id, item in value.items():
                            loadout = Loadout(**item)
                            loadouts[id] = loadout
                        self.loadouts = loadouts
        except (OSError, json.JSONDecodeError):
            pass  # we use defaults if there's an error reading or decoding the file


    def saveToFile(self):
        with open(constants.SETTINGS_PATH, "w") as file:
            settings_as_json = json.dumps(self, default=vars, indent=2)
            file.write(settings_as_json)


class Loadout:
    """
    Simple data class designed to handle the storage and management of different 
    configurations of macro keys for a particular setup.
    This class is used primarily in the settings.
    """
    def __init__(self, name, macroKeys):
        self.name = name
        self.macroKeys = macroKeys