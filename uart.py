from machine import Pin, UART
from time import sleep
import utime
import uos

# Baud rate setting for bluetooth modules
# AT+BAUD<number>
# 1 set to 1200bps
# 2 set to 2400bps
# 3 set to 4800bps
# 4 set to 9600bps (Default)
# 5 set to 19200bps
# 6 set to 38400bps
# 7 set to 57600bps
# 8 set to 115200bps

def help():

    print("AT commands (prefix 0, 1, or 2 to write to port 0, 1, or both")
    print("-"*50)
    print("AT             - Attention, should return 'OK'")
    print("AT+HELP        - Returns valid AT commands for device")
    print("AT+VERSION     - returns version number")
    print("AT+NAME        - returns current device name")
    print("AT+NAME<name>  - sets the name of the device")
    print("AT+PIN<pin>    - will set the pin e.g. 'AT+PIN4321 will set the pin to 4321")

def readUartBytes(uart, delay=1000):
    print("reading data")
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<delay:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print(resp.decode())

def readUart(uart, delay):
    response = ""
    print("reading data")
    while uart.any() > 0:
        response = uart.readline()
        print(str(response))
        sleep(delay)
 
# Create the UARTs
uart0 = UART(id=0, baudrate=115200, tx=Pin(0), rx=Pin(1))
uart1 = UART(id=1, baudrate=9600, tx=Pin(4), rx=Pin(5))

# Print a command line
print("-"*50)
print("PicoTerm")
print(uos.uname())
print("type 'quit' to exit, read<n> to read from UART<n>, or 'help' for AT commands")

# Loop
command = ""
while True and command != 'quit':
    command = input("PicoTerm>")
    if command == 'help':
        help()
    elif command == 'read0':
        print("reading bytes from UART0")
        readUartBytes(uart=uart0)
    elif command == 'read1':
        print("reading bytes from UART1")
        readUartBytes(uart=uart1)
    elif command == 'quit':
        print("-"*50)
        print("Bye")
    elif command[0:1] == '0' or command[0:1] == '1' or command[0:1] == '2':
        print("Command sent:",command[1:])
        uart = command[0:1]
        commandNL = command[1:]+'\r'+'\n'
     
        if uart != '1':
            print("writing to UART0")
            uart0.write(commandNL.encode('utf-8'))
            delay = 2500
            if command[1:] == "AT+HELP":
                delay = 7000
            readUartBytes(uart0, delay)
#            readUart(uart0, .25)

        if uart != '0':
            print("writing to UART1")
            uart1.write(commandNL.encode('utf-8'))
            delay = 5000
            if command[1:] == "AT+HELP":
                delay = 10000
            readUartBytes(uart1, delay)
#            readUart(uart1, .5)
        