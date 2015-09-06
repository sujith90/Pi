import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)


while True:
	x = random.choice([17,18,22,23,25,27])
	y = random.choice([17,18,22,23,25,27])
	if x != y:
		GPIO.output(x, GPIO.HIGH)
		GPIO.output(y, GPIO.HIGH)
		time.sleep(0.15)
		GPIO.output(x,GPIO.LOW)
		GPIO.output(y,GPIO.LOW)
