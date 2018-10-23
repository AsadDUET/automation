import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(4,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)

while True:
	GPIO.output(4,True)
	GPIO.output(17,False)
	time.sleep(3)
	GPIO.output(4,False)
	GPIO.output(17,True)
	time.sleep(3)
	print ("done")
