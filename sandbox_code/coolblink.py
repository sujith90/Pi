import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)


while True:
	GPIO.output(17,GPIO.HIGH)
	time.sleep(.1)
	GPIO.output(17,GPIO.LOW)
	GPIO.output(27,GPIO.HIGH)
	time.sleep(.1)
	GPIO.output(27,GPIO.LOW)
	GPIO.output(22,GPIO.HIGH)
	time.sleep(.1)
	GPIO.output(22,GPIO.LOW)
	GPIO.output(18,GPIO.HIGH)
	time.sleep(.1)
	GPIO.output(18,GPIO.LOW)
	GPIO.output(25,GPIO.HIGH)
	time.sleep(.1)
	GPIO.output(25,GPIO.LOW)
