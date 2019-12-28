import os
from time import sleep

def generate_snow(trigger):
    snow = []
    for i in range( 20):
        if trigger:
            snow.append("* "*20 + "\n")
            trigger = not trigger
        else:
            snow.append(" *"*20 + "\n")
            trigger = not trigger
    return snow

background = []
trigger = False
while(True):
    os.system("clear")
    trigger = not trigger
    background = generate_snow(trigger)
    print("".join(background), end="\r")
    sleep(1)