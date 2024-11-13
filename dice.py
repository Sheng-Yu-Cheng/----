import time
import random

random.seed(time.time())

def rollOneDie():
    return random.randint(1, 6)

def rollTwoDice():
    return (random.randint(1, 6), random.randint(1, 6))