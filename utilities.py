import time
import random
import uuid

def sleepTriggerKey(model):
    time.sleep(getTriggerDelayMs(model)/1000)

def sleepStrategemKey(model):
    time.sleep(getStrategemKeyDelayMs(model)/1000)

def generateUuid():
    return str(uuid.uuid4())

def getTriggerDelayMs(model):
    return random.uniform(model.settings.triggerDelay,(model.settings.triggerDelay+model.settings.triggerDelayJitter))

def getStrategemKeyDelayMs(model):
    return random.uniform(model.settings.strategemKeyDelay,(model.settings.strategemKeyDelay+model.settings.strategemKeyDelayJitter))