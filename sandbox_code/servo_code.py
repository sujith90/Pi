# External module imports
import RPi.GPIO as GPIO
import time

# Pin Definitons:
pwmPin = 17 # Broadcom pin 18 (P1 pin 12)

dc = 50# duty cycle (0-100) for PWM pin

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(pwmPin, GPIO.OUT) # PWM pin set as output
#pwm = GPIO.PWM(pwmPin, 50)  # Initialize PWM on pwmPin 100Hz frequency

# Initial state for LEDs:
#pwm.start(dc)

print("Here we go! Press CTRL+C to exit")
try:
    while 1:
	#pwm.ChangeDutyCycle(dc)
	GPIO.output(pwmPin, GPIO.HIGH)

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    #pwm.stop() # stop PWM
    GPIO.cleanup() # cleanup all GPIO
