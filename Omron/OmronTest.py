#! /usr/bin/python

# A simple Python command line tool to control an Omron MEMS Temp Sensor D6T-44L
# By Greg Griffes http://yottametric.com
# GNU GPL V3 

# Jan 2015

import smbus
import sys
import getopt
import time 
import pigpio

i2c_bus = smbus.SMBus(1)
OMRON_1=0x0a                # 7 bit I2C address of Omron MEMS Temp Sensor D6T-44L
OMRON_BUFFER_LENGTH=35            # Omron data buffer size
temperature_data=[0]*OMRON_BUFFER_LENGTH    # initialize the temperature data list

# intialize the pigpio library and socket connection to the daemon (pigpiod)
pi = pigpio.pi()              # use defaults
version = pi.get_pigpio_version()
print 'PiGPIO version = '+str(version)
handle = pi.i2c_open(1, 0x0a) # open Omron D6T device at address 0x0a on bus 1

# initialize the device based on Omron's appnote 1
result=i2c_bus.write_byte(OMRON_1,0x4c);
#print 'write result = '+str(result)

#for x in range(0, len(temperature_data)):
   #print x
   #Read all data  tem
   #temperature_data[x]=i2c_bus.read_byte(OMRON_1)
(bytes_read, temperature_data) = pi.i2c_read_device(handle, len(temperature_data))

# Display data 
print 'Bytes read from Omron D6T: '+str(bytes_read)
print 'Data read from Omron D6T : '
for x in range(bytes_read):
   print(temperature_data[x]),
#print 'done'

#Need to chop off the first 2 bytes, multiply each remaining pair
#by 256, convert to decimal, multiply by .1 then convert to Fahrenheit 
#This is a sample of the data we get with this code
#202 0 188 0 174 0 193 0 173 0 174 0 172 0 172 0 171 0 166 0 170 0 170 0 166 0 171 0 169 0 178 0 190 0 92 30
for x in range(bytes_read):
	if x > 1 and x<34 and x/2==(x+1)/2:
		temp=temperature_data[x]+temperature_data[x+1]*256 
		print x, x+1
		print temp*.1*(9/5.)+32	
