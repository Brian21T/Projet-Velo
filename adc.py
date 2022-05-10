from machine import Pin, ADC
import time
from lcd_display import lcd_setup, lcd_write, lcd_clear

# Pin definitions
adc = ADC(Pin(28))
voltage = 0

def adc_v(voltage):
    voltage = adc.read_u16()
    voltage = voltage *(3.4/65535)-0.1
    voltage = (voltage/3.4)*100
    print(voltage)
    lcd_clear()
    lcd_write("{:02.2f}%".format(voltage))
    time.sleep(1)
    return voltage
