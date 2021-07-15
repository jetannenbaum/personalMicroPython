from machine import Pin
import time

button = Pin(14, Pin.IN, Pin.PULL_UP)
x = 0

while True:
    if button.value() == 0: 
        x = x + 1
        print("Button pressed " + str(x))
        time.sleep(.25)   
