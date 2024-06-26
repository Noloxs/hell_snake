# This module defines the Settings class which provides a singleton instance to manage application settings,
# allowing settings to be loaded from a file, updated dynamically, and used across the application.
# The Settings class follows a singleton pattern.

import constants
import json
import utilities

class Loadout:
    """
    Simple data class designed to handle the storage and management of different 
    configurations of macro keys for a particular setup.
    This class is used primarily in the settings.
    """
    def __init__(self, name, macroKeys):
        self.name = name
        self.macroKeys = macroKeys

class LoadoutManager:
    def __init__(self):
        self._observers = []
        self.loadouts = {utilities.generateUuid(): self.generateDefaultLoadout("Default")}
        # Load settings from file, overriding defaults as needed
        self.loadFromFile()
        print("Loadouts initialized")

    def generateDefaultLoadout(self, name):
        # Sensible first loadout
        return Loadout( name, {
                        "1": "51", # Eagle Airstrike
                        "2": "56", # Orbital Precision Strike
                        "3": "41", # Machinegun Sentry
                        "4": "9",  # MG43 Machine gun 
                        "5": "32", # Resupply
                        "6": "0",  # Eagle Rearm
                        "7": "1",  # Reinforce
                        "8": "34", # SEAF Arty
                        "9": "7"   # Hellbomb
                        })

    # Loadout list functions
    def addLoadout(self, loadoutName) -> str:
        loadoutId = utilities.generateUuid()
        newLoadout = self.generateDefaultLoadout(loadoutName)
        self.loadouts[loadoutId] = newLoadout
        return loadoutId
    
    def deleteLoadout(self, loadoutId: str):
        if loadoutId in self.loadouts:
            del self.loadouts[loadoutId]
    
    def updateLoadout(self, loadoutId: str, loadout: Loadout):
        if loadoutId in self.loadouts:
            self.loadouts[loadoutId] = loadout

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

    def notify_change(self, **attrs):
        """
        Calls each callback in the list of observers.
        """
        for callback in self._observers:
            callback(attrs)

    def __setattr__(self, name, value):
        """
        Sets an attribute and notifies observers if the setting is not initially being populated.
        """
        self.__dict__[name] = value
        if not self.__dict__.get("_is_initializing", False):
            self.notify_change(type='setattr', name=name)  # Notify on any attribute change

    def __delattr__(self, name):
        """
        Deletes an attribute and notifies observers of the change. Probably not really used a lot.
        """
        del self.__dict__[name]
        self.notify_change(type='delattr', name=name)

    # State persistance
    def loadFromFile(self):
        try:
            with open(constants.LOADOUTS_PATH) as json_file:
                data = json.load(json_file)
                self.loadouts = {}
                for id, item in data.items():
                    loadout = Loadout(item['name'], item['macroKeys'])
                    self.loadouts[id] = loadout
            print("INFO: Loadouts loaded.")
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
            print("INFO: Loadouts saved.")
            self.notify_change(type='save')

