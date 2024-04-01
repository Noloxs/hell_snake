from strategem import Strategem
import json

class Model:
    def __init__(self):
        self.settings = {"theme": "light"}
        self.armed = False

        with open('strategems.json') as json_file:
            tmp = json.load(json_file)
        
        self.strategems = {}
        for index, item in tmp.items():
            name = item['name']
            strate = Strategem(**item)
            self.strategems.update({index: strate})
        
        self.macroKeys = {"1":"1","2":"2","3":"8","4":"5","5":"6","6":"7","7":"9","8":"4","9":"0"}

        self.macros = {}
        for key, strategemId in self.macroKeys.items():
            self.macros.update({key:self.strategems[strategemId]})

    def change_macro_binding(self, key, strategemId):
        strategem = self.strategems[strategemId]
        strategem.prepare_strategem()
        self.macros.update({key:strategem})

    def get_setting(self, setting):
        return self.settings.get(setting)

    def set_setting(self, setting, value):
        self.settings[setting] = value