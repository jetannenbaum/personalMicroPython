from machine import Pin, PWM
import utime
import time
# We are using https://github.com/blaz-r/pi_pico_neopixel
from neopixel import Neopixel

NUMBER_PIXELS = 2
STATE_MACHINE = 0
LED_PIN = 18

# The Neopixels on the Maker Pi RP2040 are the GRB variety, not RGB
strip = Neopixel(NUMBER_PIXELS, STATE_MACHINE, LED_PIN, "GRB")

# Color RGB values
red = (255, 0, 0)
yellow = (255, 150, 0)
green = (0, 255, 0)
black = (0, 0, 0)
startColors = (red, black, red, black, yellow, black, yellow, black, green, black, green, black)

def showColor(color):
    for i in range(NUMBER_PIXELS):
        strip.set_pixel(i, color)
    strip.show()

# Using Grove 3 Connector
TRIGGER_PIN = 4 # White Wire
ECHO_PIN = 5 # Yellow Wire

# Init HC-SR04P pins
trigger = Pin(TRIGGER_PIN, Pin.OUT) # send trigger out to sensor
echo = Pin(ECHO_PIN, Pin.IN) # get the delay interval back

def ping():
    trigger.low()
    utime.sleep_us(2) # Wait 2 microseconds low
    trigger.high()
    utime.sleep_us(5) # Stay high for 5 microseconds
    trigger.low()
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    return distance * .254

BUZZER_PIN = 22
buzzer = PWM(Pin(BUZZER_PIN))

def playTone():
    buzzer.duty_u16(1000)
    buzzer.freq(150)

def stopTone():
    buzzer.duty_u16(0)

# Motor definitions
FULL_POWER_LEVEL = 65024
RIGHT_FORWARD_PIN = 9
RIGHT_REVERSE_PIN = 8
LEFT_FORWARD_PIN = 11
LEFT_REVERSE_PIN = 10

right_forward = PWM(Pin(RIGHT_FORWARD_PIN))
right_reverse = PWM(Pin(RIGHT_REVERSE_PIN))
left_forward = PWM(Pin(LEFT_FORWARD_PIN))
left_reverse = PWM(Pin(LEFT_REVERSE_PIN))

def forward():
    right_forward.duty_u16(FULL_POWER_LEVEL)
    left_forward.duty_u16(FULL_POWER_LEVEL)

def forwardSlow():
    right_forward.duty_u16(FULL_POWER_LEVEL // 2)
    left_forward.duty_u16(FULL_POWER_LEVEL // 2)

def stop():
    right_forward.duty_u16(0)
    right_reverse.duty_u16(0)
    left_forward.duty_u16(0)
    left_reverse.duty_u16(0)

def reverseAndTurn():
    utime.sleep(.25)
    right_reverse.duty_u16(FULL_POWER_LEVEL // 4)
    left_reverse.duty_u16(FULL_POWER_LEVEL // 4)
    utime.sleep(1.5)
    left_reverse.duty_u16(0)
    left_forward.duty_u16(FULL_POWER_LEVEL // 4)
    utime.sleep(.75)
    stop()
    utime.sleep(.25)
    stopTone()
    forward()

for color in startColors:
    showColor(color)
    utime.sleep(.25)

forward()
while True:
    color = green      # Assume the way ahead is clear
    distance = ping()  # Check the distance
    if distance < 4:   # Obstruction ahead, slow down
        color = yellow
        forwardSlow()
    if distance < 2:   # Obstruction too close, stop, and play tone
        color = red
        stop()
        playTone()
    showColor(color)
    utime.sleep(.25)
    if color == red:  # If we stopped, back up and turn
        reverseAndTurn()