# Matt's Temperature reader
# Utilising a Micro Dot Phat for display and Temperature Sensor (DS18B20)

import os
import glob
import time
import datetime
# This imports the respective fields to use from the microdotphat's library
from microdotphat import write_string, set_decimal, clear, show, scroll

os.system('modprobe w1-gpio') 
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/' # The directory where the raw temp value is stored
device_folder = glob.glob(base_dir + '28*')[0] # The temp value is in a file that starts with '28', this looks for it
device_file = device_folder + '/w1_slave'
delay = 1

def read_temp_raw(): # Read the raw temp from the file
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close
    return lines

def read_temp(): # you can also throw in some Fahrenheit conversion here but I stripped it out
    lines = read_temp_raw()

    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()

    equals_pos = lines[1].find('t=')

    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        string_temp = str(temp_c)
        return string_temp

while True: # This prints the temp to the command line and to the microdotphat
    print(read_temp())
    time.sleep(1)
    clear()
    write_string(read_temp()[0:5] + "c", kerning=False)
    show()
    time.sleep(delay)
