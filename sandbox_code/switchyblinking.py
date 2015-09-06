import time
import random
import RPi.GPIO as GPIO
import missile

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
#GPIO.setup(22,GPIO.OUT)
#GPIO.setup(23,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)
GPIO.setup(18,GPIO.IN)

missile.setup_usb()
missile.send_move(missile.LEFT, 3000)
while True:
	if GPIO.input(18):
		GPIO.output(17, GPIO.HIGH)
		#GPIO.output(18, GPIO.HIGH)
		missile.send_cmd(missile.FIRE)
	else:
		#GPIO.output(25, GPIO.LOW)
	        GPIO.output(17, GPIO.LOW)



