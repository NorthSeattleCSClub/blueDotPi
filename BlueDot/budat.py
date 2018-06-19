from bluedot import BlueDot

import RPi.GPIO as GPIO
from time import sleep
 
GPIO.setmode(GPIO.BOARD)
 
Motor1A = 16
Motor1B = 18
Motor1E = 22
 
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

bd = BlueDot()
while True: 
##    bd.wait_for_press()
##    print("You pressed the blue dot!")

    


    
##    print("Turning motor on")
##    GPIO.output(Motor1A,GPIO.HIGH)
##    GPIO.output(Motor1B,GPIO.LOW)
##    GPIO.output(Motor1E,GPIO.HIGH)
## 
##    bd.wait_for_press()
## 
##    print("Stopping motor")
##    GPIO.output(Motor1E,GPIO.LOW)

##    sleep(0.5)

##backwards    
##    print("Turning motor on")
##    GPIO.output(Motor1A,GPIO.LOW)
##    GPIO.output(Motor1B,GPIO.HIGH)
##    GPIO.output(Motor1E,GPIO.HIGH)
## 
##    sleep(3.5)
## 
##    print("Stopping motor")
##    GPIO.output(Motor1E,GPIO.LOW)
##
##    sleep(0.5)
## 
GPIO.cleanup()
