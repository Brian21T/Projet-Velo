from machine import Pin, UART, Timer, ADC, RTC
import utime, time, math, rgb_function
from lcd_display import lcd_setup, lcd_write, lcd_clear
from rgb_function import pixels_show, pixels_black, tourne_gauche\
     , tourne_droite, red_blink, speed_wheel, gps_led, adc_wheel\
     , all_blue
from micropyGPS import MicropyGPS
from neopixel import Neopixel
from math import radians, cos, sin, asin, sqrt, atan2, degrees
from gps_distance import distance

adc = ADC(Pin(28))
voltage = 0
voltagex = 0
tim = Timer()
uart = UART(0, baudrate=38400, tx=Pin(0), rx=Pin(1))

gauche = Pin(21, Pin.IN, Pin.PULL_DOWN)
droite = Pin(22, Pin.IN, Pin.PULL_DOWN)
modes = Pin(27, Pin.IN, Pin.PULL_DOWN)
lights = Pin(26, Pin.IN, Pin.PULL_DOWN)
lumi1 = Pin(16, Pin.OUT)
lumi2 = Pin(17, Pin.OUT)
lumi3 = Pin(20, Pin.OUT)
mode = 0
lights_mode = 0
direction = 0
command = 0
x = 0 #command decode = x
rpm = ""
kmh = 0
dst = 0
attention = 0
latitude = 0
longitude = 0
heures = "0"
minutes = "0"
secondes = "0"

direction_gps = 0
var = 0
C = 0
d = 0

#---------------------------------------------------------------#
#----------------------------RGB LEDS---------------------------#
#---------------------------------------------------------------#
numpix = 30
pixels0 = Neopixel(numpix, 0, 2, "GRB")
pixels1 = Neopixel(numpix, 1, 15, "GRB")
pixels2 = Neopixel(numpix, 2, 14, "GRB")

yellow = (255, 100, 0)
orange = (255, 50, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
black = (0, 0, 0)
purple = (128, 0, 128)


color0 = red
#---------------------------------------------------------------#
#--------------------------RGB LEDS END-------------------------#
#---------------------------------------------------------------#

#---------------------------------------------------------------#
#------------------------------ADC------------------------------#
#---------------------------------------------------------------#
def adc_v():
    global voltagex, voltage
    voltage = adc.read_u16()
    voltagex = (0.0036581796897864 * voltage)-139.74246414984
#---------------------------------------------------------------#
#----------------------------ADC END----------------------------#
#---------------------------------------------------------------#
    
#---------------------------------------------------------------#
#---------------------------CLIGNOTANT--------------------------#
#---------------------------------------------------------------#
def gauche_handler(pin):
    global gauche, gauche_last, direction
    gauche.irq(handler=None)
    
    if gauche.value()==0 and \
       time.ticks_diff(time.ticks_ms(), gauche_last) > 200: #debounce
        direction = "G"
        gauche_last = time.ticks_ms()
    elif gauche.value() != 0:
        direction = "0"
        
    gauche.irq(handler=gauche_handler)
            
def droite_handler(pin):
    global droite, droite_last, direction
    droite.irq(handler=None)

    if droite.value()==0 and \
       time.ticks_diff(time.ticks_ms(), droite_last) > 200: #debounce
        direction = "D"
        droite_last = time.ticks_ms()
    elif droite.value() != 0:
        direction = "0"
        
    droite.irq(handler=droite_handler)

gauche_last = time.ticks_ms()
droite_last = time.ticks_ms()

gauche.irq(trigger = Pin.IRQ_RISING, handler = gauche_handler)
droite.irq(trigger = Pin.IRQ_RISING, handler = droite_handler)

def direction_fnc(): #Configuration des clignotants
    global direction
    if direction == "G":
        uart.write('D')
        tourne_droite()
    elif direction == "D":
        uart.write('G')
        tourne_gauche()
    elif direction == "0":
        pass
        #uart.write('0')

#---------------------------------------------------------------#
#-------------------------CLIGNOTANT FIN------------------------#
#---------------------------------------------------------------#

#---------------------------------------------------------------#
#----------------------------BOUTONS----------------------------#
#---------------------------------------------------------------#
def modes_handler(pin):
    global mode, modes, modes_last
    modes.irq(handler=None)
    
    if modes.value()==0 and time.ticks_diff(time.ticks_ms(), modes_last) > 500:
        mode += 1
        print(mode)
        modes_last = time.ticks_ms()
    elif modes.value() != 0:
        lcd_clear()
        
    modes.irq(handler=modes_handler)
            
def lights_handler(pin):
    global lights_mode, lights, lights_last
    lights.irq(handler=None)

    if lights.value()==0 and time.ticks_diff(time.ticks_ms(), lights_last) > 500:
        lights_mode += 1
        print(lights_mode)
        lights_last = time.ticks_ms()
    elif lights.value() != 0:
        lcd_clear()
     
    lights.irq(handler=lights_handler)

modes_last = time.ticks_ms()
lights_last = time.ticks_ms()

modes.irq(trigger = Pin.IRQ_RISING, handler = modes_handler)
lights.irq(trigger = Pin.IRQ_RISING, handler = lights_handler)

def modes_fnc():
    global mode, direction_gps, d, voltage
    if mode == 0:
        lcd_clear()
        pixels_black()
        pixels_show()
    if mode == 1:
        speed_wheel(kmh)
    if mode == 2:
        gps_fnc()
        gps_led(direction_gps)
        if d < 0.015:
            all_blue()
    if mode == 3:
        adc_v()
        adc_wheel(voltage)
    if mode > 3:
        mode = 0
        
        
def lights_fnc():
    global lights_mode, lumi1, lumi2, lumi3
    if lights_mode == 1:
        lumi1.low()
        lumi2.low()
        lumi3.low()
    elif lights_mode == 2:
        lumi1.high()
        lumi2.high()
        lumi3.high()
    elif lights_mode == 3:
        lumi1.toggle()
        lumi2.toggle()
        lumi3.toggle()
    elif lights_mode > 2:
        lights_mode = 1
    
#---------------------------------------------------------------#
#--------------------------BOUTONS END--------------------------#
#---------------------------------------------------------------#
        
#---------------------------------------------------------------#
#---------------------------BLUETOOTH---------------------------#
#---------------------------------------------------------------#
def bluetooth(pin):
    global command, x, rpm, kmh, dst, attention,latitude, longitude
    
    Pin(1).irq(handler=None)
    
    if uart.any():
        time.sleep(0.05) #Delay pour bien lire les donnees recu
        command = uart.read()
        x = command.decode()
        if (x[0] == 'r' and x[1] == 'o'):
            y = x.split()
            x = [s.replace("\x00", "") for s in y]
            print(x)
            rpm = (x[1])
            kmh = int(x[2])
            dst = (x[3])
        if (x[0] == 'a'):
            red_blink()
        if (x[0] == 'g' and x[1] == 'p' and x[2] == 's') :
            x = x.replace(',', '')
            coordinates_string = x.replace('-', '')
            latitude = float(coordinates_string[4:13])
            longitude = (float(coordinates_string[15:24]))*-1
            print("Latitude: {} Longitude: {} ".format( \
                  latitude,longitude))
            lcd_clear()
            lcd_write('|' '+' '\xBB' '\xBB' '\xBB')
            lcd_clear()
            lcd_write("La:  {}   Lo: {} ".format(\
                  latitude,longitude))
            time.sleep(2)
            lcd_write('|' '+' '\x00' '\x00' '\x00')
            lcd_clear()
            
        if (x[0] == 'd' and x[1] == 'a' and x[2] == 't' and x[3] == 'a') :
            lcd_clear()
            lcd_write('|' '+' '\xBB' '\xBB' '\xBB')
            lcd_clear()
            lcd_write("La:  {}   Lo: {} ".format(\
                  latitude,longitude))
            time.sleep(2)
            lcd_write('|' '+' '\x00' '\x00' '\x00')
            lcd_clear()
            uart.write("  Distance: {}Km".format(dst))
        
    Pin(1).irq(handler=bluetooth)

Pin(1).irq(trigger = Pin.IRQ_FALLING, handler = bluetooth)

#---------------------------------------------------------------#
#-------------------------BLUETOOTH END-------------------------#
#---------------------------------------------------------------#         

#---------------------------------------------------------------#
#------------------------------GPS------------------------------#
#---------------------------------------------------------------#
#GPS Module UART Connection
gps_module = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
#print gps module connection details
#print(gps_module)
#Used to Store NMEA Sentences
buff = bytearray(255)
my_gps = MicropyGPS(-4)
my_gps.satellite_data_updated()
rtc = RTC()
my_gps.satellite_data_updated()

def gps_fnc():
    global heures, minutes, secondes, var, C, d, direction_gps\
           ,latitude , longitude
    
    gps_module.readline()
    buff = str(gps_module.readline())
     
    for o in buff:
        my_gps.update(o)
        
    DMS_long = my_gps.longitude_string()
    
    angle2 = DMS_long.split("°")
    
    angle_3 = angle2[0]
    u = angle2[1] #transformer les secondes en degree
    p = u.replace("W", "")
    z = p.replace("'", "")
    angle_4 = z.replace(" ", "")
    lon = ((float(angle_3) + (float(angle_4) * 1/60))*-1)#degre pr longitude
    
    DMS_lat = my_gps.latitude_string() #degre en decimal
    angle = DMS_lat.split("°") #separer degree et secondes
    angle_1 = angle[0]
    e = angle[1] #transformer les secondes en degree
    new = e.replace("N", "")
    s = new.replace("'", "")
    angle_2 = s.replace(" ", "")
    lat = float(angle_1) + (float(angle_2) * 1/60)#degre pr latitude
    
    lat_a = lat ##from
    long_a = lon
    
#     lat_b = 45.579100##to  ST-HUBERT
#     long_b = -73.545834
#     lat_b = 45.550887 #MAISONNEUVE
#     long_b = -73.553273
#     lat_b = 45.578803598131465 #Parking au campus
#     long_b = -73.54461894165416

#     lat_b = 45.578995185409475 #Coin de rue parking
#     long_b = -73.54409558838304

    lat_b = latitude
    long_b = longitude
     
    x = cos(radians(lat_b)) * sin(radians(long_b - long_a))
    y = (cos(radians(lat_a)) * sin(radians(lat_b))) - (sin(radians(lat_a)) * cos(radians(lat_b)) * cos(radians(long_a - long_b)))

    bearing_rad = atan2(x,y)
    bearing_degree = degrees(bearing_rad)
    
    if bearing_degree > 0:
        bearing_degree = bearing_degree -360
    if bearing_degree == 0:
        var = 0
        bearing_degree = bearing_degree
    if bearing_degree < 0:
        var = 360
        bearing_degree = bearing_degree + 360
    
    lat1 = lat_a
    lon1 = long_a
    lat2 = lat_b
    lon2 = long_b
    
    if my_gps.compass_direction() == "N" :
        #direction_gps = (360 - 0) + bearing_degree
        direction_gps = bearing_degree
        if direction_gps > 360:
            direction_gps = direction_gps - 360             
    if my_gps.compass_direction() == "NNE" :
        direction_gps = (360 - 72.5) + bearing_degree
        if direction_gps > 360:
            direction_gps = direction_gps - 360       
    if my_gps.compass_direction() == "NE" :
        direction_gps = (360 - 45) + bearing_degree
        if direction_gps > 360:
            direction_gps = direction_gps - 360        
    if my_gps.compass_direction() == "ENE" :
        direction_gps = (360 - 67.5) + bearing_degree
        if direction_gps > 360:
            direction_gps = direction_gps - 360       
    if my_gps.compass_direction() == "E" :
        direction_gps = (360 - 90) + bearing_degree
        if direction_gps > 360:
            direction_gps = direction_gps - 360       
    if my_gps.compass_direction() == "ESE" :
        direction_gps = (360 - 112.5) + bearing_degree
        if direction_gps > 360:
            direction_gps = direction_gps - 360     
    if my_gps.compass_direction() == "SE" :
        direction_gps = (360 - 135) + bearing_degree
        if direction_gps > 360:
            direction_gps = direction_gps - 360       
    if my_gps.compass_direction() == "SSE" :
        direction_gps = (360 - 157.5) + bearing_degree
        if direction_gps > 360:
            direction_gps = direction_gps - 360      
    if my_gps.compass_direction() == "S" :
        direction_gps = (360 - 180) + bearing_degree
        if direction_gps > 360:
            direction_gps = direction_gps - 360      
    if my_gps.compass_direction() == "SSW" :
        direction_gps = (360 - 202.5) + bearing_degree
        if direction_gps > 360:
            direction_gps = direction_gps - 360      
    if my_gps.compass_direction() == "SW" :
        direction_gps = (360 - 225) + bearing_degree
        if direction_gps > 360:
            direction_gps = direction_gps - 360        
    if my_gps.compass_direction() == "WSW" :
        direction_gps = (360 - 247.5) + bearing_degree
        if direction_gps > 360:
            direction_gps = direction_gps - 360         
    if my_gps.compass_direction() == "W" :
        direction_gps = (360 - 270) + bearing_degree
        if direction_gps > 360:
            direction_gps = direction_gps - 360        
    if my_gps.compass_direction() == "WNW" :
        direction_gps = (360 - 292.5) + bearing_degree
        if direction_gps > 360:
            direction_gps = direction_gps - 360        
    if my_gps.compass_direction() == "NW" :
        direction_gps = (360 - 315) + bearing_degree
        if direction_gps > 360:
            direction_gps = direction_gps - 360       
    if my_gps.compass_direction() == "NNW" :
        direction_gps = (360 - 337.5) + bearing_degree
        if direction_gps > 360:
            direction_gps = direction_gps - 360      
          
    C = my_gps.compass_direction()
    d = distance(lat1, lat2, lon1, lon2)        
#---------------------------------------------------------------#
#----------------------------GPS END----------------------------#
#---------------------------------------------------------------#

#---------------------------------------------------------------#
#-----------------------------PRINT-----------------------------#
#---------------------------------------------------------------#
def lcd_print(timer):
    global rpm, kmh, dst, heures, minutes, secondes, mode, voltagex\
           ,direction_gps , d, C
    annee = max(int(my_gps.date[2]), rtc.datetime()[0])
    mois = max(int(my_gps.date[1]), rtc.datetime()[1])
    jour = max(int(my_gps.date[0]), rtc.datetime()[2])
    
    heures = max(my_gps.timestamp[0], rtc.datetime()[3])
    minutes = max(my_gps.timestamp[1], rtc.datetime()[4])
    #minutes = int(minutes)
    secondes = max(my_gps.timestamp[2], rtc.datetime()[5])
    secondes = int(secondes)
    
    if secondes == secondes:
        secondes += 1
    if secondes > 59:
        secondes = 0
        #minutes += 1

    #rtc.datetime((1, 1, 1, heures, minutes, secondes, 0, 0))
    
    rpmx = str(rpm)
    if mode == 0:
        lcd_write('|' '+' '\x00' '\x00' '\x00')
        lcd_clear()
    if mode == 1:
        lcd_write('|' '+' '\xBB' '\xBB' '\xBB')
        lcd_clear()
        lcd_write("{:02}:{:02}:{:02}   C:{:3}"\
                  .format(my_gps.timestamp[0],my_gps.timestamp[1],secondes, rpmx))
        lcd_write("Kmh:{:2}   D:{:5}".format(kmh, dst))
        
    if mode == 2:
        di = d*100
        lcd_write('|' '+' '\xBB' '\xBB' '\xBB')
        lcd_clear()
        lcd_write("D:{:05.2f}    {:3}  {:5.2f}".format(di, C, direction_gps))
        print("D:{:05.2f}    {:3}  {:5.2f}".format(di, C, direction_gps))
    if mode == 3:
        lcd_write('|' '+' '\xBB' '\xBB' '\xBB')
        lcd_clear()
        lcd_write("Batterie: {:02.2f}%".format(voltagex)

tim.init(period=1000, mode=Timer.PERIODIC, callback=lcd_print)
#---------------------------------------------------------------#
#---------------------------PRINT END---------------------------#
#---------------------------------------------------------------#

pixels_black()
pixels_show()
print("Start")
lcd_setup()

while True:
    gps_fnc()
    direction_fnc()
    modes_fnc()
    lights_fnc()   
    time.sleep(0.2)
    










