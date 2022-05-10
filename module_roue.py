from machine import Timer, Pin, UART
import utime, time

uart = UART(0, baudrate=38400, tx=Pin(0), rx=Pin(1))
reedsw = Pin(27, Pin.IN, Pin.PULL_DOWN)

a = 0
flag = 0
temps = 0
pulse = 0
temps = 0
rpm = 0
circ = 0
distance_m = 0
km_h = 0
command = 0
commandD = 0

def int_handler(pin):
    global flag, start_timer, temps
    reedsw.irq(handler=None)
    if flag == 0:
        if reedsw.value() == 1 and time.ticks_diff(time.ticks_ms(), start_timer) > 50:
            flag = 1
            temps = time.ticks_diff(time.ticks_ms(), start_timer)/1000
    reedsw.irq(handler=int_handler)
    start_timer = time.ticks_ms()

def calc_speed(radius):
    global a, start_timer, temps, rpm, circ, distance_m, km_h, flag
    if flag==1:
        flag = 0 
        if temps != 0:
            a +=1
            rpm = 1/(temps) * 60
            circ = (2*3.1416)*radius
            distance = circ/100000
            km_s = distance/(temps)
            km_h = km_s*3600
            distance_m = (distance*a)*1000
            #print("RPM: {:4.0f}  KM/H: {:3.0f}  Distance: {:5.2f} m".format(rpm, km_h, distance_m))
            
            rpmx = str("{:1.0f}".format(rpm))
            distancex = str("{:1.0f}".format(distance_m))
            km_hx = str("{:1.0f}".format(km_h))
            
            uart.write(rpmx +" "+km_hx + " " +distancex)
            #time.sleep(0.20)
            print(rpmx +" "+ km_hx + " " +distancex)
            
print("--Start--")

start_timer = time.ticks_ms()
reedsw.irq(trigger=machine.Pin.IRQ_RISING, handler=int_handler)

while True:
    if uart.any():
        command = uart.read()
        print(command)
#         commandD = command.decode().strip("\r\n").strip("\x00")
#         print("Module Arrière:", commandD)
    #uart.write("Allo")
    #print("{:3.0f}".format(rpm))
    calc_speed(34.3)
    #time.sleep(2)
    time.sleep(0.20)
