import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(13, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
while True:
	GPIO.output(13, 1) 
	GPIO.output(33, 1)
	GPIO.output(10, 1)

