from machine import Pin
import time

green = Pin(18, Pin.OUT)
yellow = Pin(19, Pin.OUT)
red = Pin(20, Pin.OUT)

green.high()
yellow.high()
red.high()

state = 0
while True:
    if state == 0:
        green.low()
        yellow.high()
        red.high()
    if state == 1:
        green.high()
        yellow.low()
        red.high()
    if state == 2:
        green.high()
        yellow.high()
        red.low()
    state = state + 1
    if state > 2:
        state = 0
    time.sleep(1)
