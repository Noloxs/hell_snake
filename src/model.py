from src.strategem import Strategem
import json
from src import utilities, key_parser_pynput

class Model:
    def __init__(self):
        self.isArmed = False

        with open('src/strategems.json') as json_file:
            tmp = json.load(json_file)
        
        self.strategems = {}
        for index, item in tmp.items():
            name = item['name']
            strate = Strategem(**item)
            self.strategems.update({index: strate})
        
        self.settings = self.load_settings()

    def update_macro_binding(self, key, strategemId):
        strategem = self.strategems[strategemId]
        self.currentLoadout.macroKeys[key] = strategemId
        self.macros.update({key:strategem})
    
    def add_loadout(self, loadoutName):
        self.settings.loadouts.update({utilities.generateUuid(): Loadout(loadoutName, {"1":"1"})})

    def delete_loadout(self, loadoutId):
        self.settings.loadouts.pop(loadoutId)
    
    def get_next_loadout(self):
        if len(self.settings.loadouts) > 0:
            return next(iter(self.settings.loadouts.keys()))
        return None

    def update_loadout(self, id, loadout):
        self.settings.loadouts[id] = loadout

    def set_active_loadout(self, id):
        self.currentLoadoutId = id
        self.macros = {}
        if id == None:
            self.currentLoadout = None
            self.macroKeys = None
        else:
            self.currentLoadout = self.settings.loadouts[id]
            self.macroKeys = self.currentLoadout.macroKeys
            for key, strategemId in self.macroKeys.items():
                self.macros.update({key:self.strategems[strategemId]})      

    def set_armed(self, isArmed):
        self.isArmed = isArmed

    def load_settings(self):
        with open('settings.json') as json_file:
            data = json.load(json_file)

        settings = Settings()

        if 'triggerKey' in data:
            settings.setTriggerKey(data['triggerKey'])

        if 'triggerDelay' in data:
            settings.setTriggerDelay(data['triggerDelay'])
        
        if 'triggerDelayJitter' in data:
            settings.setTriggerDelayJitter(data['triggerDelayJitter'])
        
        if 'strategemKeys' in data:
            settings.setStrategemKeys(data['strategemKeys'])
        
        if 'strategemKeyDelay' in data:
            settings.setStrategemKeyDelay(data['strategemKeyDelay'])

        if 'strategemKeyDelayJitter' in data:
            settings.setStrategemKeyDelayJitter(data['strategemKeyDelayJitter'])
        
        if 'selectedExecutor' in data:
            settings.setExecutor(data['selectedExecutor'])
        
        if 'globalArmKey' in data:
            settings.setGlobalArmKey(data['globalArmKey'])
        
        if 'globalArmMode' in data:
            settings.setGlobalArmMode(data['globalArmMode'])
        
        if 'view_framework' in data:
            settings.setViewFramework(data['view_framework'])
        
        if 'loadouts' in data:
            loadouts = {}
            for id, item in data['loadouts'].items():
                loadout = Loadout(**item)
                loadouts.update({id: loadout})
            settings.setLoadouts(loadouts)

        return settings

class Settings:
    def __init__(self):
        self.loadouts = {utilities.generateUuid():Loadout("Profile 1", {"1":"1"})}
        self.triggerKey = "ctrl"
        self.triggerDelay = 100
        self.triggerDelayJitter = 30
        self.strategemKeys = ["w", "a", "s", "d"]
        self.strategemKeyDelay = 30
        self.strategemKeyDelayJitter = 20
        self.selectedExecutor = "pynput"
        self.globalArmKey = None
        self.globalArmMode = "toggle"
        self.view_framework = "pyqt5"

    def setTriggerKey(self, key):
        self.triggerKey = key
    
    def setTriggerDelay(self, delay):
        self.triggerDelay = delay
    
    def setTriggerDelayJitter(self, jitter):
        self.triggerDelayJitter = jitter
    
    def setStrategemKeys(self, strategemKeys):
        self.strategemKeys = strategemKeys
    
    def setStrategemKeyDelay(self, delay):
        self.strategemKeyDelay = delay
    
    def setStrategemKeyDelayJitter(self, jitter):
        self.strategemKeyDelayJitter = jitter

    def setExecutor(self, executor_name):
        self.selectedExecutor = executor_name
    
    def setGlobalArmKey(self, key):
        self.globalArmKey = key
    
    def setGlobalArmMode(self, mode):
        self.globalArmMode = mode
    
    def setViewFramework(self, framework):
        self.view_framework = framework
    
    def setLoadouts(self, loadouts):
        self.loadouts = loadouts

class Loadout:
    def __init__(self, name, macroKeys):
        self.name = name
        self.macroKeys = macroKeys