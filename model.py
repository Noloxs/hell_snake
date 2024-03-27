from strategem import Strategem
import json

class Model:
    def __init__(self):
        self.settings = {"theme": "light"}
        self.armed = False

        with open('strategems.json') as json_file:
            strategems = json.load(json_file)

        self.macros = {
                        "1": Strategem(**strategems['1']),
                        "2": Strategem(**strategems["2"]),
                        "3": Strategem(**strategems["8"]),
                        "4": Strategem(**strategems["5"]),
                        "5": Strategem(**strategems["6"]),
                        "6": Strategem(**strategems["7"]),
                        "7": Strategem(**strategems["9"]),
                        "8": Strategem(**strategems["4"]),
                        "9": Strategem(**strategems["0"])
                        }

    def get_setting(self, setting):
        return self.settings.get(setting)

    def set_setting(self, setting, value):
        self.settings[setting] = value