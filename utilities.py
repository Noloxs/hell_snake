import time
import random
import uuid

def sleepMs(delayMs, jitterMs):
    time.sleep(getDelayWithJitterMs(delayMs, jitterMs)/1000)

def generateUuid():
    return str(uuid.uuid4())

def getDelayWithJitterMs(delayMs, jitterMs):
    return random.uniform(delayMs,(delayMs+jitterMs))