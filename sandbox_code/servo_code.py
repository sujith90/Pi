import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

p = GPIO.PWM(18, 50)  # channel=12 frequency=50Hz
p.start(0)
try:
    while 1:
	p.start(0)
        for dc in range(40, 101, 5):
	    print "dc: ",dc/10.0
            p.ChangeDutyCycle(dc/10.0)
            time.sleep(1)
        '''for dc in range(50, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(.5)
	'''
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()

