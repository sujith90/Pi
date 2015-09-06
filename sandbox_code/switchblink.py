import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(17, GPIO.OUT)
GPIO.setup(26,GPIO.IN)
GPIO.setup(25,GPIO.OUT)
GPIO.setup(18,GPIO.IN)


#energize the circuit
#GPIO.output(25, GPIO.HIGH)

#de-energize the circuit (no current to the switch)
GPIO.output(25, GPIO.HIGH)

#initialize the LED to OFF
GPIO.output(17, GPIO.LOW) #led off

while True:
	if GPIO.input(18):
		GPIO.output(17, GPIO.HIGH)
	else:
		GPIO.output(17, GPIO.LOW)


#while True:
#	if GPIO.input(26):
#		while GPIO.input(26):
#			GPIO.output(17, GPIO.HIGH) #led on
#	GPIO.output(17, GPIO.LOW) #led off
#GPIO.output(25, GPIO.HIGH)
