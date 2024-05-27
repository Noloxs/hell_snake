import time
import random
import uuid

def sleepTriggerKey(model):
    time.sleep(getTriggerDelayMs(model)/1000)

def sleepStratagemKey(model):
    time.sleep(getStratagemKeyDelayMs(model)/1000)

def generateUuid():
    return str(uuid.uuid4())

def getTriggerDelayMs(model):
    return random.uniform(model.settings.triggerDelay,(model.settings.triggerDelay+model.settings.triggerDelayJitter))

def getStratagemKeyDelayMs(model):
    return random.uniform(model.settings.stratagemKeyDelay,(model.settings.stratagemKeyDelay+model.settings.stratagemKeyDelayJitter))