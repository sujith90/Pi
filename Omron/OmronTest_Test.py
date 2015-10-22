#! /usr/bin/python

# A simple Python command line tool to control an Omron MEMS Temp Sensor D6T-44L
# By Greg Griffes http://yottametric.com
# GNU GPL V3 

# Jan 2015

from random import randint

'''
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
 
'''


# define the function blocks
def center_block():
    #GPIO.output(17, GPIO.HIGH)
    print "Center Block: Turn on LED & No movement"

def top_center():
    #GPIO.output(17, GPIO.LOW)
    print "Top Center: Turn off LED & Move Camera UP"
    
def bottom_center():
    #GPIO.output(17, GPIO.LOW)
    print "Bottom Center: Turn off LED & Move Camera DOWN"

def right_center():
    #GPIO.output(17, GPIO.LOW)
    print "Right Center: Turn off LED & Move Camera RIGHT"
    
def left_center():
    #GPIO.output(17, GPIO.LOW)
    print "Left Center: Turn off LED & Move Camera LEFT"

def top_left():
    #GPIO.output(17, GPIO.LOW)
    print "Top Left: Turn off LED & Move Camera UP_LEFT"

def top_right():
    #GPIO.output(17, GPIO.LOW)
    print "Top Right: Turn off LED & Move Camera UP_RIGHT"

def bottom_left():
    #GPIO.output(17, GPIO.LOW)
    print "Bottom Left: Turn off LED & Move Camera BOTTOM_LEFT"
    
def bottom_right():
    #GPIO.output(17, GPIO.LOW)
    print "Bottom Right: Turn off LED & Move Camera BOTTOM_RIGHT"

# map the inputs to the function blocks
function = {
            1 : top_left,
            2 : top_center,
            3 : top_center,
            4 : top_right,
            5 : left_center,
            6 : center_block,
            7 : center_block,
            8 : right_center,
            9 : left_center,
            10 : center_block,
            11 : center_block,
            12 : right_center,
            13 : bottom_left,
            14 : bottom_center,
            15 : bottom_center,
            16 : bottom_right
}


 
bytes_read = [202, 0, 188, 0, 174, 0, 193, 0, 173, 0, 174, 0, 172, 0, 172, 0, 171, 0, 166, 0, 170, 0, 170, 0, 166, 0, 171, 0, 169, 0, 178, 0, 190, 0, 92, 30];
r = randint(1,16)*2
bytes_read[r] = 200
for x, byte in enumerate(bytes_read):
   if x%2==0 and x!=0 and x!=34:
      temp = byte*.1*(9/5.)+32
      print x/2, byte, temp
    
function[bytes_read.index(max(bytes_read[2:-1]))/2]()     
      
     
      

