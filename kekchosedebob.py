from machine import Timer, Pin, UART
import utime, time

uart = UART(0, baudrate=38400, tx=Pin(0), rx=Pin(1))
print("test")


def gps_data():
    if uart.any():
        command = uart.read()
        x=command.decode()
        print("commande recu: ", x)
#         print(command)
#         print("Decode",x)
        if (x[0] == 'g' and x[1] == 'p' and x[2] == 's') :
            coordinates = x.split()
            coordinate_latitude = coordinates[1]
            coordinate_longitude = coordinates[2]
            print("Latitude : ", coordinate_latitude)
            print("Longitude : ", coordinate_longitude)

        elif (x[0] == 'd' and x[1] == 'a' and x[2] == 't' and x[3] == 'a') :
            print("commande recu pour envoyer les data au tel")
            uart.write(" voici les donnees")
    
while True:
    gps_data()
    time.sleep(0.1)