import board
import busio
import pwmio
from microcontroller import Pin
from adafruit_motor import motor

def readUartBytes(uart):
    data = uart.read(1)
    if data is not None:
        data_string = ''.join([chr(b) for b in data])
    else:
        data_string = ''
    return (data_string)

def stopMotors(leftMotor, rightMotor):
    leftMotor.throttle = 0
    rightMotor.throttle = 0

def turnLeft(leftMotor, rightMotor):
    leftMotor.throttle = -.5
    rightMotor.throttle = .5
 
def turnRight(leftMotor, rightMotor):
    leftMotor.throttle = .5
    rightMotor.throttle = -.5

def moveForward(leftMotor, rightMotor):
    leftMotor.throttle = 1
    rightMotor.throttle = 1

def moveBackward(leftMotor, rightMotor):
    leftMotor.throttle = -.5
    rightMotor.throttle = -.5
 
# Initialize UART
uart = busio.UART(board.GP0, board.GP1, baudrate=9600)

# Initialize DC motors
m1a = pwmio.PWMOut(board.GP8, frequency=50)
m1b = pwmio.PWMOut(board.GP9, frequency=50)
motor1 = motor.DCMotor(m1a, m1b)
m2a = pwmio.PWMOut(board.GP10, frequency=50)
m2b = pwmio.PWMOut(board.GP11, frequency=50)
motor2 = motor.DCMotor(m2a, m2b)

dir = 's'
while True:
    newDir = str(readUartBytes(uart)).lower()
    if newDir is not None:
        dir = newDir
    if dir == 'f':
        moveForward(motor1, motor2)
    elif dir == 'b':
        moveBackward(motor1, motor2)
    elif dir == 'l':
        turnLeft(motor2, motor1)
    elif dir == 'r':
        turnRight(motor2, motor1)
    elif dir == 's':
        stopMotors(motor1, motor2)