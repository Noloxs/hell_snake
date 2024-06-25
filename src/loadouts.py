# This module defines the Settings class which provides a singleton instance to manage application settings,
# allowing settings to be loaded from a file, updated dynamically, and used across the application.
# The Settings class follows a singleton pattern.

import constants
import json
import utilities

class LoadoutManager:
    def __init__(self):
        self._observers = []
        self._currentLoadout = None
        self.loadouts = {utilities.generateUuid(): Loadout("Loadout 1", {"1": "1"})}
        # Load settings from file, overriding defaults as needed
        self.loadFromFile()
        print("Loadouts initialized")

    # Loadout manipulation functions
    def getCurrentLoadout(self):
        if self._currentLoadout is None:
            self._currentLoadout = next(iter(self.loadouts.keys()))
        return self._currentLoadout

    def setCurrentLoadout(self, loadoutId):
        if loadoutId not in self.loadouts:
            self._currentLoadout = None
            print("ERR: Attempt to set invalid loadout.")
        else:
            self._currentLoadout = loadoutId

    # Observer pattern functions
    def attach_change_listener(self, callback):
        """
        Adds a callback to the list of observers if it's not already present.
        """
        if callback not in self._observers:
            self._observers.append(callback)

    def detach_change_listener(self, callback):
        """
        Removes a callback from the list of observers if present.
        """
        try:
            self._observers.remove(callback)
        except ValueError:
            pass

    def notify_change(self):
        """
        Calls each callback in the list of observers.
        """
        for callback in self._observers:
            callback()

    def __setattr__(self, name, value):
        """
        Sets an attribute and notifies observers if the setting is not initially being populated.
        """
        self.__dict__[name] = value
        if not self.__dict__.get("_is_initializing", False):
            self.notify_change()  # Notify on any attribute change

    def __delattr__(self, name):
        """
        Deletes an attribute and notifies observers of the change. Probably not really used a lot.
        """
        del self.__dict__[name]
        self.notify_change()

    # State persistance
    def loadFromFile(self):
        try:
            with open(constants.LOADOUTS_PATH) as json_file:
                data = json.load(json_file)
                self.loadouts = {}
                for id, item in data.items():
                    loadout = Loadout(item['name'], item['macroKeys'])
                    self.loadouts[id] = loadout
            return True
        except (OSError, json.JSONDecodeError):
            return False


    def saveToFile(self):
        loadouts_as_json = {}
        for id, loadout in self.loadouts.items():
            item = {"name": loadout.name,'macroKeys': loadout.macroKeys}
            loadouts_as_json[id] = item
        with open(constants.LOADOUTS_PATH, "w") as file:
            settings_as_json = json.dumps(loadouts_as_json, indent=2)
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

    def to_json(self):
        return {'name': self.name, 'macroKeys': self.macroKeys}