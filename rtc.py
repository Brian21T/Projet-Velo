from machine import RTC
import time

rtc = RTC()
rtc.datetime((2017, 8, 23, 2, 12, 48, 0, 0)) # set a specific date and
                                             # time, eg. 2017/8/23 1:12:48
while True:
    print(rtc.datetime()) # get date and time
    time.sleep(1)    
