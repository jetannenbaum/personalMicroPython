from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
 
x = 0
y = 0
for dir in range(4):
    step = 1
    if (dir == 1 or dir == 3):
        step = -1
    for z in range(0, 13):
        oled.fill(0)    
        oled.show()
        x += step
        y += 1
        oled.text("Hello Sunshine", x, y)
        oled.show()
        time.sleep(.25)


