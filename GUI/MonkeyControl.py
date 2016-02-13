import RPi.GPIO as GPIO
import time



class MonkeyControl():

	def init(self):
		print("MonkeyControl Init Started...")
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		# PIN 19 is to control Logic for monkey movement
		# GPIO.output(19, 0) to turn on monkey movement
		# GPIO.output(19, 1) to turn off monkey movement
		GPIO.setup(19, GPIO.OUT) #***Uncomment this when Monkey is integrated into Circuit.***
		print("MonkeyControl Init Ended...")	
	
	def monkey_on(self):
		GPIO.output(19, 0) #***Uncomment this when Monkey is integrated into Circuit.***
		print("MonkeyControl: Monkey On")

	def monkey_off(self):
		GPIO.output(19, 1) #***Uncomment this when Monkey is integrated into Circuit.***
		print("MonkeyControl: Monkey Off")
		

