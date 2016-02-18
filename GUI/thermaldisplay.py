#!/etc/bin/python2.7

import pygame, time, sys
from omrond6t import *
from pygame.locals import *
import RPi.GPIO as GPIO

class Tracking():

	def init_tracking(self):
		print "\n\ntracking init started...\n\n"
		
		self.omron = OmronD6T(arraySize=16)
		self.temperature = []
		self.time_delay = .1 #
		self.environment_temp = 70 # Temp difference bet
		self.temp_difference = 10
		self.prev_temp_diff =  0 #PID's I value
		self.motor_movement = .25
		self.presenceDetected = True
		self.awayFlag = False
		

		
		#GPIO Initializers
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(18, GPIO.OUT)
		
		#GPIO Initializers for RGB LED
		GPIO.setup(23, GPIO.OUT)
		GPIO.setup(24, GPIO.OUT)
		GPIO.setup(25, GPIO.OUT)

		self.p = GPIO.PWM(18, 50)  # channel=12 frequency=50Hz
		self.dutycycle = 7
		self.prevDutycycle = 7
		self.maxCell = -1
		self.p.start(0)
				
		for dc in range(20, 120, 10):
			print "dc: ",dc/10.0
			self.p.ChangeDutyCycle(dc/10.0)
			time.sleep(.2)
		for dc in range(120, 70, -10):
			print "dc: ",dc/10.0
			self.p.ChangeDutyCycle(dc/10.0)
			time.sleep(.2)
		
		# map the inputs to the function blocks
		self.function = {
			    1 : self.Cell_One,
			    2 : self.Cell_Two,
			    3 : self.Cell_Three,
			    0 : self.Cell_Four
		}
		

		self.ii = 1
		print "\n\ntracking init finished!\n\n"


	def temp_to_rgb(self,temp):
	  if temp < 76:
	    return (0, 0, 192)
	  elif temp >= 76 and temp < 90:
	    return (255, 128, 0)
	  elif temp > 90:
	    return (255, 0, 0)


	# define the function blocks

	def Cell_One(self):
	    row = [self.temperature[self.maxCell]]
	    row.insert(1,self.temperature[self.maxCell+1])
	    row.insert(2,self.temperature[self.maxCell+2])
	    row.insert(3,self.temperature[self.maxCell+3])
	#multiply  based on max-min
	    self.setDutyCycle(row)

	def Cell_Two(self):
	    row = [self.temperature[self.maxCell-1]]
	    row.insert(1,self.temperature[self.maxCell])
	    row.insert(2,self.temperature[self.maxCell+1])
	    row.insert(3,self.temperature[self.maxCell+2])
	    self.setDutyCycle(row)

	def Cell_Three(self):
	    row = [self.temperature[self.maxCell-2]]
	    row.insert(1,self.temperature[self.maxCell-1])
	    row.insert(2,self.temperature[self.maxCell])
	    row.insert(3,self.temperature[self.maxCell+1])
	    self.setDutyCycle(row)
	    
	def Cell_Four(self):
	    row = [self.temperature[self.maxCell-3]]
	    row.insert(1,self.temperature[self.maxCell-2])
	    row.insert(2,self.temperature[self.maxCell-1])
	    row.insert(3,self.temperature[self.maxCell])
	    self.setDutyCycle(row)

	def getPresenceInfo(self):
		self.getTempData()
		
		if max(self.temperature) > self.environment_temp:
			self.presenceDetected = True
			self.awayFlag = True
			self.prevDutycycle = self.dutycycle
		else:
			if self.awayFlag:
				self.awayFlag = False
				for dc in range(40, 120, 10):
					print "dc: ",dc/10.0
					self.p.ChangeDutyCycle(dc/10.0)
					time.sleep(.2)
					self.getTempData()
					if max(self.temperature) > self.environment_temp:
						self.presenceDetected = True
						self.awayFlag = True
						break
						
			

			self.presenceDetected = False
		return self.presenceDetected
	
	def getTempData(self):
		self.temperature = list(self.omron.read())[1]
		#print self.temperature

	def turnMotorOff(self):
		GPIO.output(18,1)

	def setDutyCycle(self,values):
	    
	    m = 8 #sensitivity of change in temp 
	    self.prev_temp_diff = 0
	    if(((max(values)-min(values)) > self.temp_difference)):
		'''
		and (prev_temp_diff != (max(values)-min(values))). lockout break mechanism
		'''
		self.prev_temp_diff = (max(values)-min(values))
		multiplier = [(values[0]-min(values))/m,(values[1]-min(values))/m,(values[2]-min(values))/m,(values[3]-min(values))/m]
		mValues = [multiplier[0]*values[0],multiplier[1]*values[1],multiplier[2]*values[2],multiplier[3]*values[3]]
		mulAvg  = sum(mValues)/len(mValues)
		weightedValue = [mValues[0]/mulAvg, mValues[1]/mulAvg, mValues[2]/mulAvg, mValues[3]/mulAvg]
		
		ServoValues = [weightedValue[0]*1,weightedValue[1]*2,weightedValue[2]*3,weightedValue[3]*4]
		
		DC = sum(ServoValues)/len(ServoValues)

		max_index = values.index(max(values))
		'''
		print "\n"
		print "DC: ", DC, "\n"
		print "DutyCycle: ", self.dutycycle, "\n"
		print "max_index: ", max_index, "\n"
		print "\n"
		'''

	

		if(DC > 3.00 and max_index != 1 and max_index != 2 ):
			self.dutycycle = self.dutycycle + self.motor_movement
			self.p.ChangeDutyCycle(self.dutycycle)
		elif(DC < 2.0 and max_index != 1 and max_index != 2 ):
			self.dutycycle = self.dutycycle - self.motor_movement
			self.p.ChangeDutyCycle(self.dutycycle)
		'''
		else:
			print "\nCentered!\n"
		'''
		time.sleep(.05)	
	
	'''
	    else:
	    	print "Row: ", values, "\tMax-Min: ", (max(values)-min(values))
		print "DC NOT CHANGED! ", "\n"
	'''



	def tracking(self):

		print("In Tracking")
		#while self.threadExit == False:
		
		#print self.temperature

		#Can this calculation be done before the loop? BP
		if self.getPresenceInfo():
			self.maxCell = self.temperature.index(max(self.temperature))
			self.function[(self.maxCell+1)%4]()

			
			

		
		if (self.ii < 20):
			self.presenceDetected = True
		


		time.sleep(self.time_delay)
		
		self.ii += 1
	

