# This module defines the Settings class which provides a singleton instance to manage application settings,
# allowing settings to be loaded from a file, updated dynamically, and used across the application.
# The Settings class follows a singleton pattern.

import constants
import json

class SettingsManager:

    def __init__(self):
        self._observers = []
        # Load defaults, protecting against missing values
        self.loadDefaults()
        # Load settings from file, overriding defaults as needed
        self.loadFromFile()
        ## Consider no version to be version 1
        if not hasattr(self, "version") or self.version < 2:
            self.migrate_1_to_2()
        if self.version == 2:
            self.migrate_2_to_3()
        if self.version == 3:
            self.migrate_3_to_4()
        if self.version == 4:
            self.migrate_4_to_5()
        print("Settings initialized")

    # Settings notifications
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
        The attrs parameter allows calling the notify method with additional arguments,
        which are packed into an event dictionary. This allows for more specific notifications
        to be sent to observers.
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

    def loadDefaults(self):
        """
        We load a base set of settings, in case the user has no settings file.
        """
        self.triggerKey = "ctrl"
        self.stratagemKeys = ["w", "a", "s", "d"]
        self.selectedExecutor = constants.EXECUTOR_PYNPUT
        self.key_listener = constants.LISTENER_PYNPUT
        self.theme = constants.THEME_AUTO
        self.globalArmKey = None
        self.globalArmMode = constants.ARM_MODE_TOGGLE
        self.view_framework = constants.VIEW_PYQT5
        self.nextLoadoutKey = "+"
        self.prevLoadoutKey = "-"

    def loadFromFile(self):
        try:
            with open(constants.SETTINGS_PATH) as json_file:
                data = json.load(json_file)
                if 'loadouts' in data:
                    pass
                self.parseSettings(data)
            return True
        except (OSError, json.JSONDecodeError):
            return False

    def parseSettings(self, settings_data):
        for attribute, value in settings_data.items():
            # Exclude 'loadouts' from this general assignment because it's already processed
            if attribute != 'loadouts':
                setattr(self, attribute, value)


    def saveToFile(self):
        with open(constants.SETTINGS_PATH, "w") as file:
            # Custom function for filtering attributes
            def filter_attributes(obj):
                return {
                    key: value for key, value in vars(obj).items() 
                    if not key.startswith('_')  # Exclude private attributes
                }
            settings_as_json = json.dumps(self, default=filter_attributes, indent=2)
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

    def migrate_2_to_3(self):
        self.version = 3

        #TODO Migrate values to executor?

        if hasattr(self, "triggerDelay"):
            del self.triggerDelay
        if hasattr(self, "triggerDelayJitter"):
            del self.triggerDelayJitter
        if hasattr(self, "stratagemKeyDelay"):
            del self.stratagemKeyDelay
        if hasattr(self, "stratagemKeyDelayJitter"):
            del self.stratagemKeyDelayJitter
        print("Settings migrated to version 3. Remember to save.")

    def migrate_3_to_4(self):
        self.version = 4

        if hasattr(self, 'loadouts'):
            delattr(self, 'loadouts')

        print("Settings migrated to version 4. Remember to save.")

    def migrate_4_to_5(self):
        self.version = 5

        # Add key_listener setting if not present (default to pynput for backwards compat)
        if not hasattr(self, 'key_listener'):
            self.key_listener = constants.LISTENER_PYNPUT

        # Add theme setting if not present (default to auto)
        if not hasattr(self, 'theme'):
            self.theme = constants.THEME_AUTO

        print("Settings migrated to version 5. Remember to save.")
