import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class s_motor(object):
	def __init__(self,a1,a2,b1,b2,delay):
		self.a1=a1
		self.a2=a2
		self.b1=b1
		self.b2=b2
		self.delay=delay
		GPIO.setup(self.a1,GPIO.OUT)
		GPIO.setup(self.a2,GPIO.OUT)
		GPIO.setup(self.b1,GPIO.OUT)
		GPIO.setup(self.b2,GPIO.OUT)
		self.set_step(0,0,0,0)
	def forward(self,steps):
		for i in range(0,steps):
			self.set_step(1,0,1,0)
			time.sleep(self.delay)
			self.set_step(0,1,1,0)
			time.sleep(self.delay)
			self.set_step(0,1,0,1)
			time.sleep(self.delay)
			self.set_step(1,0,0,1)
			time.sleep(self.delay)

	def backward(self,steps):
		for i in range(0,steps):
			self.set_step(1,0,0,1)
			time.sleep(self.delay)
			self.set_step(0,1,0,1)
			time.sleep(self.delay)
			self.set_step(0,1,1,0)
			time.sleep(self.delay)
			self.set_step(1,0,1,0)
			time.sleep(self.delay)
	def set_step(self,a1,a2,b1,b2):
		GPIO.output(self.a1,a1)
		GPIO.output(self.a2,a2)
		GPIO.output(self.b1,b1)
		GPIO.output(self.b2,b2)
m1=s_motor(2,3,4,17,.01)
m1.forward(100)
m1.backward(100)
