# LED Matrix message scroller demo.

import bitmapfont
from machine import Pin
import utime
from neopixel import NeoPixel

# Configuration:
SPEED          = 10.0    # Scroll speed in pixels per second.
NEOPIXEL_PINS  = [12, 13, 14, 15, 16, 17, 18, 19]  #Pins for the neopixel displays
ROWS           = 8  # Each display has 8 pixels
COLS           = 8  # There are 8 neopixel modules
strips         = [] # a list of neopixel strips


for neopixel_pin in NEOPIXEL_PINS:
    strips.append(NeoPixel(Pin(neopixel_pin), ROWS))

def write_pixel_value(x, y, value):
    if y >= 0 and y < ROWS and x >=0 and x < COLS:
        strips[x][ROWS - 1 - y] = value

def fill(value):
    for x in range(COLS):
        for y in range(ROWS):
            write_pixel_value(x, y, value)

def show():
    for i in range(COLS):
        strips[i].write()
    
def write_pixel(x, y):
    write_pixel_value(x, y, (1,4,1))

def scroll_text(message):
    with bitmapfont.BitmapFont(ROWS, COLS, write_pixel) as bf:
        # Global state:
        pos = ROWS                 # X position of the message start.
        message_width = bf.width(message)   # Message width in pixels.
        last = utime.ticks_ms()             # Last frame millisecond tick time.
        speed_ms = SPEED / 1000.0           # Scroll speed in pixels/ms.
        # Main loop:
        while True:
            # Compute the time delta in milliseconds since the last frame.
            current = utime.ticks_ms()
            delta_ms = utime.ticks_diff(current, last)
            last = current
            
            # Compute position using speed and time delta.
            pos -= speed_ms*delta_ms
            if pos < -message_width:
                pos = ROWS
                
            # Clear the matrix and draw the text at the current position.
            fill((0,0,0))
            bf.text(message, int(pos), 0)
            
            # Update the pixels.
            show()

scroll_text('MicroPython Rocks!')