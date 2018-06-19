import RPi.GPIO as GPIO
from time import sleep
 
GPIO.setmode(GPIO.BOARD)
 
Motor1A = 16
Motor1B = 18
Motor1E = 22
 
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

##set up the pwm
##pwm = GPIO.PWM(Motor1E, 100)
##
##pwm.start(0)
##GPIO.output(Motor1E, GPIO.HIGH)

for i in range(5):

## forward      //high, low, high
    print("Turning motor on")
##    pwm.ChangeDutyCycle(30)
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
 
    sleep(3.5)
 
    print("Stopping motor")
##    pwm.ChangeDutyCycle(0)
    GPIO.output(Motor1E,GPIO.LOW)

    sleep(2)

## backwards    //low, high, high
    print("Turning motor on")
##    pwm.ChangeDutyCycle(90)
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
 
    sleep(3.5)
 
    print("Stopping motor")
##    pwm.ChangeDutyCycle(0)
    GPIO.output(Motor1E,GPIO.LOW)

    sleep(2)

GPIO.output(Motor1E, GPIO.LOW)
 
GPIO.cleanup()
