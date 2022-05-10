from machine import Pin, UART, I2C
from micropyGPS import MicropyGPS
import math
from lcd_display import lcd_setup, lcd_write, lcd_clear
from rgb_function import pixels_show, pixels_black, tourne_gauche\
     , tourne_droite, red_blink, speed_wheel, gps_led, adc_wheel
from machine import RTC
from test import distance

#Import utime library to implement delay
import utime, time

#GPS Module UART Connection
gps_module = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

#print gps module connection details
print(gps_module)

#Used to Store NMEA Sentences
buff = bytearray(255)

my_gps = MicropyGPS(-4)
rtc = RTC()

my_gps.satellite_data_updated()

var = 0

while True:   
    gps_module.readline()
    buff = str(gps_module.readline())
    #print(buff)
    
    for o in buff:
        my_gps.update(o)

    ##calcul_longitude()
    ##calcul_latitude()
        
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

    lat_b = 45.578803598131465 #Campus
    long_b = -73.54461894165416
     
    x = math.cos(math.radians(lat_b)) * math.sin(math.radians(long_b - long_a))
    y = (math.cos(math.radians(lat_a)) * math.sin(math.radians(lat_b))) - (math.sin(math.radians(lat_a)) * math.cos(math.radians(lat_b)) * math.cos(math.radians(long_a - long_b)))

    bearing_rad = math.atan2(x,y)
    bearing_degree = math.degrees(bearing_rad)
    
    
    if bearing_degree > 0:
        bearing_degree = bearing_degree -360
    if bearing_degree == 0:
        var = 0
        bearing_degree = bearing_degree
    if bearing_degree < 0:
        var = 360
        bearing_degree = bearing_degree + 360
        
    #print(bearing_degree)
    #print("Latitude:{} Longitude:{} ".format(lat, lon))
    #print("time: "+str(my_gps.timestamp))
    
    lat1 = lat_a
    lon1 = long_a
    lat2 = lat_b
    lon2 = long_b
    
    d = distance(lat1, lat2, lon1, lon2)
    #print(distance(lat1, lat2, lon1, lon2), "K.M")
    print("{} Km".format(d))

#     r = 6371 #radius of Earth (KM)
#     p = 0.017453292519943295  #Pi/180
#     a = 0.5 - math.cos((lat2-lat1)*p)/2 + math.cos(lat1*p)*math.cos(lat2*p) * (1-math.cos((lon2-lon1)*p)) / 2
# 
#     d = 2 * r * math.asin(math.sqrt(a)) #2*R*asin


    #print(d)
    #print(my_gps.compass_direction())

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

    annee = max(int(my_gps.date[2]), rtc.datetime()[0])
    mois = max(int(my_gps.date[1]), rtc.datetime()[1])
    jour = max(int(my_gps.date[0]), rtc.datetime()[2])
    
    heures = max(my_gps.timestamp[0], rtc.datetime()[3])
    minutes = max(my_gps.timestamp[1], rtc.datetime()[4])
    minutes = int(minutes)
    secondes = max(my_gps.timestamp[2], rtc.datetime()[5])
    secondes = int(secondes)
    
   
    if secondes == secondes:
        secondes += 1
    if secondes > 59:
        secondes = 0
        minutes += 1
#     heures = my_gps.timestamp[0]
#     minutes = my_gps.timestamp[1]
#     secondes = my_gps.timestamp[2]
#     secondes = int(secondes)
  
#     rtc.datetime((22, 5, 3, heures, minutes, secondes, 0, 0))
    
#     print(bearing_degree)
#     print("Latitude:{} Longitude:{} ".format(lat, lon))
#     print("time: "+str(my_gps.timestamp)) 
#     lcd_clear()
#     lcd_write("La{:2} B{} Lo{:5}".format(lat,bearing_degree, lon))
#     lcd_clear()
#     lcd_write("B: {:5}  C: {}D: {}".format(direction_gps, C, d))
#     print(my_gps.compass_direction())
#     print("direction",direction_gps)
#     print("bearing  ",bearing_degree)
#     lcd_clear()
#     lcd_write("D:{:3.2f}    {:3} B:{:3.2f}".format(direction_gps, C, bearing_degree))

    #Clock
#     print("RTC time:", rtc.datetime())
#     print("GPS time:", my_gps.timestamp)
#     print("Clk time: {:02}:{:02}:{:02}".format(heures,minutes,secondes))
#     lcd_clear()
#     lcd_write("{:02}:{:02}:{:02}".format(heures,minutes,secondes))
#     print(my_gps.date_string())

#     lcd_clear()
#     lcd_write("{}    {}  {}".format(lat_a,long_b, d))

#     gps_led(direction_gps)
#     
    time.sleep(0.3)
    


