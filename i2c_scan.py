from machine import Pin, I2C

i2c=I2C(0,sda=Pin(4), scl=Pin(5), freq=400000)

devices = i2c.scan()

if len(devices) == 0:
    print("No i2c device !")
else:
    print('i2c devices found:',len(devices))
    
for device in devices:
    print("Digi address: ", device)
    print("Hexa address: ",hex(device))
