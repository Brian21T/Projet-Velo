from machine import Pin, I2C
import time

lcd = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
lcd.scan()

addr = 0x72

def lcd_write(x):
    #lcd.writeto(addr,'\x7C') 
    lcd.writeto(addr,x)

def lcd_clear():
    lcd_write('\x7C') 
    lcd_write('\x2D')

def lcd_setup():
    lcd_write('\x7C') 
    #lcd_writeto('|' '+' '\x7C' '\xFF' '\x00')
    #lcd_writeto('|' '\x06')
    lcd_write('|' '+' '\xBB' '\xBB' '\xBB') #Full white
    #lcd_write('|' '+' '\x00' '\x00' '\x00') #No light
    lcd_clear()
    
lcd_clear()    
lcd_write('|' '+' '\xBB' '\xBB' '\xBB')
lcd_clear()
lcd_write("    Bonjour!")
time.sleep(2)
lcd_write('|' '+' '\x00' '\x00' '\x00')
lcd_clear()

# lcd_setup()   
# lcd_write("Please work!")
# time.sleep(2)
# lcd_clear()



