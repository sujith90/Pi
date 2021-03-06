import RPi.GPIO as GPIO
import time



class LedControl():

	def init(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		# PIN 19 is to control Logic for monkey movement
		# GPIO.output(19, 0) to turn on monkey movement
		# GPIO.output(19, 1) to turn off monkey movement
		#GPIO.setup(19, GPIO.OUT)

		GPIO.setup(23, GPIO.OUT)
		GPIO.setup(12, GPIO.OUT)
		GPIO.setup(16, GPIO.OUT)
	
	
	def ledOnRed(self):
		GPIO.output(23, 1) 
		GPIO.output(12, 0)
		GPIO.output(16, 0)

	def ledOnGreen(self):
		GPIO.output(23, 0) 
		GPIO.output(12, 1)
		GPIO.output(16, 0)

	def ledOnBlue(self):
		GPIO.output(23, 0) 
		GPIO.output(12, 0)
		GPIO.output(16, 1)

	def ledOff(self):
		GPIO.output(23, 0) 
		GPIO.output(12, 0)
		GPIO.output(16, 0)

	def cycleColors(self):
		#Red
		GPIO.output(23, 1) 
		GPIO.output(12, 0)
		GPIO.output(16, 0)

		time.sleep(0.25)

		GPIO.output(23, 0) 
		GPIO.output(12, 0)
		GPIO.output(16, 0)

		time.sleep(0.25)

		#Green
		GPIO.output(23, 0) 
		GPIO.output(12, 1)
		GPIO.output(16, 0)

		time.sleep(0.25)

		GPIO.output(23, 0) 
		GPIO.output(12, 0)
		GPIO.output(16, 0)

		time.sleep(0.25)
	
		#Blue
		GPIO.output(23, 0) 
		GPIO.output(12, 0)
		GPIO.output(16, 1)

		time.sleep(0.25)

		GPIO.output(23, 0) 
		GPIO.output(12, 0)
		GPIO.output(16, 0)




		
		

		
