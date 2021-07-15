import time
from machine import Pin, I2C
from vl53l0x import VL53L0X
from ssd1306 import SSD1306_I2C

print("setting up i2c")
i2cToF = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
i2cDisplay=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)

print("creating vl53lox object")
tof = VL53L0X(i2cToF)

print("creating display object")
oled = SSD1306_I2C(128, 64, i2cDisplay)

print("setting up LEDs")
green = Pin(18, Pin.OUT)
yellow = Pin(19, Pin.OUT)
red = Pin(20, Pin.OUT)

green.high()
yellow.high()
red.high()

# the measuting_timing_budget is a value in ms, the longer the budget, the more accurate the reading.
tof.set_measurement_timing_budget(40000)

print("getting and displaying range")
while True:
    oled.fill(0)    

    # Start ranging
    measureMM = tof.ping() - 25
    oled.text(str(measureMM) + " mm", 0, 0)
    measureIn = round(measureMM / 25.4, 2)
    oled.text(str(measureIn) + " inches", 0, 10)
    oled.show()
    if measureIn < 4:
        green.high()
        yellow.high()
        red.low()
    elif measureIn < 8:
        green.high()
        yellow.low()
        red.high()
    else:
        green.low()
        yellow.high()
        red.high()
    time.sleep(.25)
    