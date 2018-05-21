from bluedot import BlueDot
from signal import pause

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


def dpad(pos):
    if pos.top:
##        print("up")
        ## forward      //high, low, high
##        print("Turning motor on")
##    pwm.ChangeDutyCycle(30)
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.HIGH)
    elif pos.bottom:
##        print("down")
##        backwards    //low, high, high
##        print("Turning motor on")
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor1E,GPIO.HIGH)
    else:
        stop()

def stop():
##    print('I should be stopping')
    GPIO.output(Motor1E, GPIO.LOW)
    
while True:
    bd.wait_for_press()
    bd.when_pressed = dpad
##    bd.when_moved = dpad
    bd.wait_for_release()
    stop()

pause()
GPIO.cleanup()

