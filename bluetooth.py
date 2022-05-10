from machine import Timer, Pin, UART
import utime, time

uart = UART(0, baudrate=38400, tx=Pin(0), rx=Pin(1))

while True:
    if uart.any():
        command = uart.read()
        print(command)
        
    time.sleep(1)

    
