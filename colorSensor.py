from machine import Pin, PWM
from time import sleep
from neopixel import NeoPixel
from tcs34725 import *  

NUMBER_PIXELS = 2
LED_PIN = 18

#Define the pin as output
pin = Pin(LED_PIN, Pin.OUT)

# Define the NeoPixel Strip
strip = NeoPixel(pin, NUMBER_PIXELS)

# Color RGB values
red = (255, 0, 0)
yellow = (255, 150, 0)
green = (0, 255, 0)
black = (0, 0, 0)
startColors = (red, black, red, black, yellow, black, yellow, black, green, black, green, black)

def showColor(color):
    for i in range(NUMBER_PIXELS):
        strip[i] = color
    strip.write()

# Motor definitions
FULL_POWER_LEVEL = 65024
RIGHT_FORWARD_PIN = 11
RIGHT_REVERSE_PIN = 10
LEFT_FORWARD_PIN = 9
LEFT_REVERSE_PIN = 8

right_forward = PWM(Pin(RIGHT_FORWARD_PIN))
right_reverse = PWM(Pin(RIGHT_REVERSE_PIN))
left_forward = PWM(Pin(LEFT_FORWARD_PIN))
left_reverse = PWM(Pin(LEFT_REVERSE_PIN))

def forwardSlow():
    right_reverse.duty_u16(0)
    left_reverse.duty_u16(0)
    right_forward.duty_u16(FULL_POWER_LEVEL // 2)
    left_forward.duty_u16(FULL_POWER_LEVEL // 2)
      
def stop():
    right_forward.duty_u16(0)
    right_reverse.duty_u16(0)
    left_forward.duty_u16(0)
    left_reverse.duty_u16(0)
 
tcs = TCS34725(scl=Pin(1), sda=Pin(0))         # instance of TCS34725 on ESP32
if not tcs.isconnected:                        # terminate if not connected
    print("Terminating...")
    sys.exit()
tcs.gain = TCSGAIN_LOW
tcs.integ = TCSINTEG_HIGH
tcs.autogain = True                                 # use autogain!

for color in startColors:
    showColor(color)
    sleep(.5)
   
while True:                                     # forever
    Clear, Red, Green, Blue = tcs.colors # obtain all counts
    if Green > Red + 500:
        forwardSlow()
        color = green
    else:
        stop()
        color = red
    showColor(color)
    sleep(.05)                                    # interval between reads

