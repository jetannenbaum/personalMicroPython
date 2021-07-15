from machine import Pin, PWM, UART, I2C
from vl53l0x import VL53L0X
import time # sleep

POWER_LEVEL = 65025

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

def stopWheels(leftFwdPWM,rightFwdPWM,leftRevPWM,rightRevPWM):
    leftFwdPWM.duty_u16(0)
    rightFwdPWM.duty_u16(0)
    leftRevPWM.duty_u16(0)
    rightRevPWM.duty_u16(0)

def spin_wheels(leftPWM, rightPWM):
    leftPWM.duty_u16(POWER_LEVEL)
    rightPWM.duty_u16(POWER_LEVEL)

def readUartBytes(uart):
    resp = b""
    if uart.any():
        resp = b"".join([resp, uart.read(1)])
    return (resp.decode())

dir = "s"

while True:
    newDir = readUartBytes(uart1)
    if newDir != "":
        dir = newDir
        stopWheels(right_forward, left_forward, left_reverse, right_reverse)

    measureMM = tof.ping() - 25
    measureIn = round(measureMM / 25.4, 2)

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