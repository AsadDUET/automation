import RPi.GPIO as GPIO
import time


#sonar program
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
TRIG = 18
ECHO = 16
sonar_readings=[15,15,15,15,15]
print ("Distance Measurement In Progress")
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
def read_sonar():
    for i in range(5):
        GPIO.output(TRIG, False)
        print ("Waiting For Sensor To Settle" )
        time.sleep(.05)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        while GPIO.input(ECHO)==0:
            pulse_start = time.time()
        while GPIO.input(ECHO)==1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        if (distance>=3 and distance<=28):
            sonar_readings[i]=distance
        else:
            sonar_readings[i]=15
    distance=sum(sonar_readings)/len(sonar_readings)
    print ("Distance:",distance,"cm")
while True:
    read_sonar()
