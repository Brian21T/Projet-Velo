import time
from neopixel import Neopixel

numpix = 30
pixels0 = Neopixel(numpix, 0, 2, "GRB")
pixels1 = Neopixel(numpix, 1, 15, "GRB")
pixels2 = Neopixel(numpix, 2, 14, "GRB")

white = (255, 255, 255)
yellow = (255, 100, 0)
orange = (255, 50, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
black = (0, 0, 0)
purple = (128, 0, 128)

color0 = red
 
# pixels.brightness(50)
# pixels.fill(orange)
# pixels.set_pixel_line_gradient(3, 13, green, blue)
# pixels.set_pixel_line(14, 16, red)
# pixels.set_pixel(20, (255, 255, 255))
def pixels_show():
    pixels0.show()
    pixels1.show()
    pixels2.show()
    
def pixels_black():
    pixels0.fill(black)
    pixels1.fill(black)
    pixels2.fill(black)
 
def red_blink():
    pixels0.brightness(100)
    pixels2.brightness(100)
    pixels2.set_pixel_line(0, 3, red)
    pixels0.set_pixel(0, red)
    pixels_show()
    time.sleep(0.2)
    pixels2.set_pixel_line(0, 3, black)
    pixels0.set_pixel(0, black)
    pixels_show()
    time.sleep(0.1)

def tourne_gauche():
    pixels0.brightness(100)
    pixels0.set_pixel_line(0, 2, yellow)
    pixels_show()
    time.sleep(0.3)
    pixels0.set_pixel_line(0, 2, black)
    pixels_show()
    time.sleep(0.05)

def tourne_droite():
    pixels1.brightness(100)
    pixels1.set_pixel_line(2, 3, yellow)
    pixels2.set_pixel(0, yellow)
    pixels_show()
    time.sleep(0.3)
    pixels1.set_pixel_line(2, 3, black)
    pixels2.set_pixel(0, black)
    pixels_show()
    time.sleep(0.05)
    
def speed_wheel(kmh):
    pixels0.brightness(100)
    pixels1.brightness(100)
    pixels2.brightness(100)
    
    if kmh == 0:
        pixels_black()
        pixels_show()
    elif 0 <= kmh < 7:
        pixels_black()
        pixels0.set_pixel(0, green)
        pixels0.set_pixel_line(1, 3, black)
        pixels1.set_pixel_line(0, 3, black)
        pixels_show()
    elif 7 <= kmh < 14:
        pixels_black()
        pixels0.set_pixel_line_gradient(0, 1, green, yellow)
        pixels0.set_pixel_line(2, 3, black)
        pixels1.set_pixel_line(0, 3, black)
        pixels_show()
    elif 14 <= kmh < 21:
        pixels_black()
        pixels0.set_pixel_line_gradient(0, 2, green, yellow)
        pixels0.set_pixel(3, black)
        pixels1.set_pixel_line(0, 3, black)
        pixels_show()
    elif 21 <= kmh < 28:
        pixels_black()
        pixels0.set_pixel_line_gradient(0, 3, green, yellow)
        pixels1.set_pixel_line(0, 3, black)
        pixels_show()
    elif 28 <= kmh < 35:
        pixels_black()
        pixels0.set_pixel_line_gradient(0, 3, green, yellow)
        pixels1.set_pixel(0, orange)
        pixels1.set_pixel_line(1, 3, black)
        pixels_show()
    elif 35 <= kmh < 42:
        pixels_black()
        pixels0.set_pixel_line_gradient(0, 3, green, yellow)
        pixels1.set_pixel_line_gradient(0, 1, orange, red)
        pixels1.set_pixel_line(1, 3, black)
        pixels_show()
    elif 49 <= kmh < 56:
        pixels_black()
        pixels0.set_pixel_line_gradient(0, 3, green, yellow)
        pixels1.set_pixel_line_gradient(0, 2, orange, red)
        pixels1.set_pixel(3, black)
        pixels2.set_pixel(0, black)
        pixels_show()
    elif 56 <= kmh < 64:
        pixels_black()
        pixels0.set_pixel_line_gradient(0, 3, green, yellow)
        pixels1.set_pixel_line_gradient(0, 3, orange, red)
        pixels2.set_pixel(0, black)
        pixels_show()
    elif 64 < kmh:
        pixels_black()
        pixels_show()
        pixels0.set_pixel_line_gradient(0, 3, green, yellow)
        pixels1.set_pixel_line_gradient(0, 3, orange, red)
        pixels2.set_pixel(0, purple)
        pixels0.show()
        pixels1.show()
        pixels2.show()
              
def gps_led(direction_gps):
    pixels0.brightness(100)
    pixels1.brightness(100)
    pixels2.brightness(100)
    
    if direction_gps > 345 or 0 <= direction_gps <= 15:
        pixels_black()
        pixels0.set_pixel(3, black)
        pixels1.set_pixel(0, green)
        pixels1.set_pixel(1, black)
        pixels_show()
    elif 15 < direction_gps <= 45 :
        pixels_black()
        pixels1.set_pixel(0, black)
        pixels1.set_pixel(1, green)
        pixels1.set_pixel(2, black)
        pixels_show()
    elif 45 < direction_gps <= 75 :
        pixels_black()
        pixels1.set_pixel(1, black)
        pixels1.set_pixel(2, green)
        pixels1.set_pixel(3, black)        
        pixels_show()
    elif 75 < direction_gps <= 105 :
        pixels_black()
        pixels1.set_pixel(2, black)
        pixels1.set_pixel(3, green)
        pixels2.set_pixel(0, black)
        pixels_show()
    elif 105 < direction_gps <= 135 :
        pixels_black()
        pixels1.set_pixel(3, black)
        pixels2.set_pixel(0, green)
        pixels2.set_pixel(1, black)        
        pixels_show()
    elif 135 < direction_gps <= 165 :
        pixels_black()
        pixels2.set_pixel(0, black)
        pixels2.set_pixel(1, green)
        pixels2.set_pixel(2, black)
        pixels_show()
    elif 165 < direction_gps <= 195 :
        pixels_black()
        pixels2.set_pixel(1, black)
        pixels2.set_pixel(2, green)
        pixels2.set_pixel(3, black)
        pixels_show()
    elif 195 < direction_gps <= 225 :
        pixels_black()
        pixels2.set_pixel(2, black)
        pixels2.set_pixel(3, green)
        pixels0.set_pixel(1, black)
        pixels_show()
    elif 225 < direction_gps <= 255:
        pixels_black()
        pixels2.set_pixel(3, black)
        pixels0.set_pixel(0, green)
        pixels0.set_pixel(1, black)
        pixels_show()
    elif 255 < direction_gps <= 285:
        pixels_black()
        pixels0.set_pixel(0, black)
        pixels0.set_pixel(1, green)
        pixels0.set_pixel(2, black)
        pixels_show()
    elif 255 < direction_gps <=315:
        pixels_black()
        pixels0.set_pixel(1, black)
        pixels0.set_pixel(2, green)
        pixels1.set_pixel(3, black)
        pixels_show()
    elif 315 < direction_gps <= 345:
        pixels_black()
        pixels0.set_pixel(2, black)
        pixels0.set_pixel(3, green)
        pixels1.set_pixel(0, black)
        pixels_show()


def adc_wheel(voltage):
    pixels0.brightness(100)
    pixels1.brightness(100)
    pixels2.brightness(100)
    if 38200 <= voltage < 40478:
        pixels_black()
        pixels2.set_pixel(2, red)       
        pixels2.set_pixel_line(2,3, black)#off
        pixels_show()
    elif 40478 <= voltage < 42756:
        pixels_black()
        pixels2.set_pixel(2, black)#off
        pixels2.set_pixel_line_gradient(2,3, red, orange)   
        pixels0.set_pixel(0, black)#off
        pixels_show()
    elif 42756 <= voltage < 45034:
        pixels_black()
        pixels0.set_pixel(0, orange)
        pixels2.set_pixel_line_gradient(2,3, red, orange)
        pixels0.set_pixel(1, black)#off
        pixels_show()
    elif 45034 <= voltage < 47312:
        pixels_black()
        pixels0.set_pixel_line_gradient(0,1, orange, orange)
        pixels2.set_pixel_line_gradient(2,3, red, red)
        pixels0.set_pixel(2, black)#off
        pixels_show()
    elif 47312 <= voltage < 49590:
        pixels_black()
        pixels0.set_pixel_line_gradient(0,2, orange, orange)
        pixels2.set_pixel_line_gradient(2,3, red, red)
        pixels0.set_pixel(3, black)#off
        pixels_show()
    elif 49590 <= voltage < 51868:
        pixels_black()
        pixels0.set_pixel_line_gradient(0,3, red, yellow)
        pixels2.set_pixel_line_gradient(2,3, red, red)
        pixels1.set_pixel(0, black)#off
        pixels_show()
    elif 51868 <= voltage < 54146:
        pixels_black()
        pixels1.set_pixel(0, yellow)
        pixels0.set_pixel_line_gradient(0,3, red, yellow)
        pixels2.set_pixel_line_gradient(2,3, red, red)
        pixels1.set_pixel(1, black)#off
        pixels_show()
    elif 54146 <= voltage < 56424:
        pixels_black()
        pixels1.set_pixel_line_gradient(0,1, yellow, yellow)
        pixels0.set_pixel_line_gradient(0,3, red, orange)
        pixels2.set_pixel_line_gradient(2,3, red, red)
        pixels1.set_pixel(2, black)#off
        pixels_show()
    elif 56424 <= voltage < 58702:
        pixels_black()
        pixels1.set_pixel_line_gradient(0,2, yellow, yellow)
        pixels0.set_pixel_line_gradient(0,3, red, orange)
        pixels2.set_pixel_line_gradient(2,3, red, red)
        pixels1.set_pixel(3, black)
        pixels_show()
    elif 58702 <= voltage < 60980:
        pixels_black()
        pixels1.set_pixel_line_gradient(0,3, yellow, green)
        pixels0.set_pixel_line_gradient(0,3, red, orange)
        pixels2.set_pixel_line_gradient(2,3, red, red)
        pixels2.set_pixel(0, black)
        pixels_show()     
    elif 60980 <= voltage < 63258:
        pixels_black()
        pixels1.set_pixel_line_gradient(0,3, yellow, green)
        pixels0.set_pixel_line_gradient(0,3, red, orange)
        pixels2.set_pixel_line_gradient(2,3, red, red)
        pixels2.set_pixel(0, green)
        pixels2.set_pixel(1, black)
        pixels_show()    
    elif 63258 <= voltage < 65535:
        pixels_black()
        pixels1.set_pixel_line_gradient(0,3, yellow, green)
        pixels0.set_pixel_line_gradient(0,3, red, orange)
        pixels2.set_pixel_line_gradient(2,3, red, red)
        pixels2.set_pixel_line_gradient(0,1, green, green)
        pixels_show()
    
def all_blue():
    pixels0.fill(blue)
    pixels1.fill(blue)
    pixels2.fill(blue)
    pixels_show()
    time.sleep(0.2)
    pixels_black()
    pixels_show()
    time.sleep(0.2)
    
# while True:
#     voltage = 65000
#     red_blink()
#     tourne_gauche()
#     tourne_droite()
#     pixels_black()
#     pixels_show()
#     adc_wheel(voltage)
#     time.sleep(1)

    





