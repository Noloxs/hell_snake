from strategem import Strategem
import json

class Model:
    def __init__(self):
        self.armed = False

        with open('strategems.json') as json_file:
            tmp = json.load(json_file)
        
        self.strategems = {}
        for index, item in tmp.items():
            name = item['name']
            strate = Strategem(**item)
            self.strategems.update({index: strate})
        
        self.settings = self.load_settings()
        
        self.set_active_loadout(next(iter(self.settings.loadouts.keys())))

    def change_macro_binding(self, key, strategemId):
        strategem = self.strategems[strategemId]
        strategem.prepare_strategem()
        self.macros.update({key:strategem})
    
    def set_active_loadout(self, id):
        self.currentLoadout = self.settings.loadouts[id]
        self.macroKeys = self.currentLoadout.macroKeys
        self.macros = {}
        for key, strategemId in self.macroKeys.items():
            self.macros.update({key:self.strategems[strategemId]})
    
    def load_settings(self):
        with open('settings.json') as json_file:
            data = json.load(json_file)

        settings = Settings()

        if 'triggerKey' in data:
            settings.setTriggerKey(data['triggerKey'])
        
        if 'selectedExecutor' in data:
            settings.setExecutor(data['selectedExecutor'])
        
        if 'loadouts' in data:
            loadouts = {}
            for id, item in data['loadouts'].items():
                loadout = Loadout(**item)
                loadouts.update({id: loadout})
            settings.setLoadouts(loadouts)

        return settings

class Settings:
    def __init__(self):
        self.loadouts = {"id":Loadout("Profile 1", {"1":"1"})}
        self.triggerKey = "ctrl"
        self.selectedExecutor = "pynput"

    def setTriggerKey(self, key):
        self.triggerKey = key
    
    def setExecutor(self, executor_name):
        self.selectedExecutor = executor_name
    
    def setLoadouts(self, loadouts):
        self.loadouts = loadouts

class Loadout:
    def __init__(self, name, macroKeys):
        self.name = name
        self.macroKeys = macroKeys