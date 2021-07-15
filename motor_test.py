from machine import Pin, PWM, UART, I2C
from vl53l0x import VL53L0X
import time # sleep

POWER_LEVEL = 65025

# lower right pins with USB on top
RIGHT_FORWARD_PIN = 7
RIGHT_REVERSE_PIN = 6
LEFT_FORWARD_PIN = 9
LEFT_REVERSE_PIN = 8

right_forward = PWM(Pin(RIGHT_FORWARD_PIN))
right_reverse = PWM(Pin(RIGHT_REVERSE_PIN))
left_forward = PWM(Pin(LEFT_FORWARD_PIN))
left_reverse = PWM(Pin(LEFT_REVERSE_PIN))

uart1 = UART(id=1, baudrate=9600, tx=Pin(4), rx=Pin(5))

i2cToF = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
tof = VL53L0X(i2cToF)

left_sensor = Pin(14, Pin.IN)
right_sensor = Pin(15, Pin.IN)

def stopWheels(leftFwdPWM,rightFwdPWM,leftRevPWM,rightRevPWM):
    leftFwdPWM.duty_u16(0)
    rightFwdPWM.duty_u16(0)
    leftRevPWM.duty_u16(0)
    rightRevPWM.duty_u16(0)

def spin_wheel(pwm):
        pwm.duty_u16(POWER_LEVEL)
        time.sleep(3)
        pwm.duty_u16(0)
        time.sleep(2)

def spin_wheels(leftPWM, rightPWM):
    leftPWM.duty_u16(POWER_LEVEL)
    rightPWM.duty_u16(POWER_LEVEL)

def readUartBytes(uart):
    resp = b""
    if uart.any():
        resp = b"".join([resp, uart.read(1)])
    return (resp.decode())

dir = "s"
old_left = 2
old_right = 2

while True:
    newDir = readUartBytes(uart1)
    if newDir != "":
        dir = newDir
        stopWheels(right_forward, left_forward, left_reverse, right_reverse)

    if dir == "a":
        left = left_sensor.value()
        right = right_sensor.value()
        print('L: ' + str(left) + ' R: ' + str(right) + ' OL: ' + str(old_left) + ' OR: ' + str(old_right)) 
        if old_left != left or old_right != right:
            stopWheels(right_forward, left_forward, left_reverse, right_reverse)
        if left == 1 and right == 0:
            spin_wheels(left_forward, right_reverse)
        if left == 0 and right == 1:
            spin_wheels(left_reverse, right_forward)
        if left == 0 and right == 0:
            spin_wheels(left_forward, right_forward)
        if left == 1 and right == 1:
            dir = "s"
        old_left = left
        old_right = right
    else:
        measureMM = tof.ping() - 25
        measureIn = round(measureMM / 25.4, 2)

        print(str(measureIn))
        
        if measureIn < 4:
            stopWheels(right_forward, left_forward, left_reverse, right_reverse)
            spin_wheels(left_reverse, right_reverse)
            time.sleep(.25)
            dir = "s"

        if dir == "f":
            spin_wheels(left_forward, right_forward)

        if dir == "b":
            spin_wheels(left_reverse, right_reverse)

        if dir == "l":
            spin_wheels(left_reverse, right_forward)

        if dir == "r":
            spin_wheels(left_forward, right_reverse)

        if dir == "s":
            stopWheels(right_forward, left_forward, left_reverse, right_reverse)