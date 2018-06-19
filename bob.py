#!/usr/bin/env python

from bluedot import BlueDot
from signal import pause

from SunFounder_TB6612 import TB6612
from SunFounder_PCA9685 import PCA9685
from SunFounder_PCA9685 import Servo
import filedb

# proprietary_code
class Back_Wheels(object):
	''' Back wheels control class '''
	Motor_A = 17
	Motor_B = 27

	PWM_A = 4
	PWM_B = 5

	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "back_wheels.py":'

	def __init__(self, debug=False, bus_number=1, db="config"):
		''' Init the direction channel and pwm channel '''
		self.forward_A = True
		self.forward_B = True

		self.db = filedb.fileDB(db=db)

		self.forward_A = int(self.db.get('forward_A', default_value=1))
		self.forward_B = int(self.db.get('forward_B', default_value=1))

		self.left_wheel = TB6612.Motor(self.Motor_A, offset=self.forward_A)
		self.right_wheel = TB6612.Motor(self.Motor_B, offset=self.forward_B)

		self.pwm = PCA9685.PWM(bus_number=bus_number)
		def _set_a_pwm(value):
			pulse_wide = self.pwm.map(value, 0, 100, 0, 4095)
			self.pwm.write(self.PWM_A, 0, pulse_wide)

		def _set_b_pwm(value):
			pulse_wide = self.pwm.map(value, 0, 100, 0, 4095)
			self.pwm.write(self.PWM_B, 0, pulse_wide)

		self.left_wheel.pwm  = _set_a_pwm
		self.right_wheel.pwm = _set_b_pwm

		self._speed = 0

		self.debug = debug
		if self._DEBUG:
			print self._DEBUG_INFO, 'Set left wheel to #%d, PWM channel to %d' % (self.Motor_A, self.PWM_A)
			print self._DEBUG_INFO, 'Set right wheel to #%d, PWM channel to %d' % (self.Motor_B, self.PWM_B)

	def forward(self):
		''' Move both wheels forward '''
		self.left_wheel.forward()
		self.right_wheel.forward()
		if self._DEBUG:
			print self._DEBUG_INFO, 'Running forward'

	def backward(self):
		''' Move both wheels backward '''
		self.left_wheel.backward()
		self.right_wheel.backward()
		if self._DEBUG:
			print self._DEBUG_INFO, 'Running backward'

	def stop(self):
		''' Stop both wheels '''
		self.left_wheel.stop()
		self.right_wheel.stop()
		if self._DEBUG:
			print self._DEBUG_INFO, 'Stop'

	@property
	def speed(self, speed):
		return self._speed

	@speed.setter
	def speed(self, speed):
		self._speed = speed
		''' Set moving speeds '''
		self.left_wheel.speed = self._speed
		self.right_wheel.speed = self._speed
		if self._DEBUG:
			print self._DEBUG_INFO, 'Set speed to', self._speed

	@property
	def debug(self):
		return self._DEBUG

	@debug.setter
	def debug(self, debug):
		''' Set if debug information shows '''
		if debug in (True, False):
			self._DEBUG = debug
		else:
			raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

		if self._DEBUG:
			print self._DEBUG_INFO, "Set debug on"
			self.left_wheel.debug = True
			self.right_wheel.debug = True
			self.pwm.debug = True
		else:
			print self._DEBUG_INFO, "Set debug off"
			self.left_wheel.debug = False
			self.right_wheel.debug = False
			self.pwm.debug = False

	def ready(self):
		''' Get the back wheels to the ready position. (stop) '''
		if self._DEBUG:
			print self._DEBUG_INFO, 'Turn to "Ready" position'
		self.left_wheel.offset = self.forward_A
		self.right_wheel.offset = self.forward_B
		self.stop()

	def calibration(self):
		''' Get the front wheels to the calibration position. '''
		if self._DEBUG:
			print self._DEBUG_INFO, 'Turn to "Calibration" position'
		self.speed = 50
		self.forward()
		self.cali_forward_A = self.forward_A
		self.cali_forward_B = self.forward_B

	def cali_left(self):
		''' Reverse the left wheels forward direction in calibration '''
		self.cali_forward_A = (1 + self.cali_forward_A) & 1
		self.left_wheel.offset = self.cali_forward_A
		self.forward()

	def cali_right(self):
		''' Reverse the right wheels forward direction in calibration '''
		self.cali_forward_B = (1 + self.cali_forward_B) & 1
		self.right_wheel.offset = self.cali_forward_B
		self.forward()

	def cali_ok(self):
		''' Save the calibration value '''
		self.forward_A = self.cali_forward_A
		self.forward_B = self.cali_forward_B
		self.db.set('forward_A', self.forward_A)
		self.db.set('forward_B', self.forward_B)
		self.stop()

##########################################################################

class Front_Wheels(object):
	''' Front wheels control class '''
	FRONT_WHEEL_CHANNEL = 0

	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "front_wheels.py":'

	def __init__(self, debug=False, db="config", bus_number=1, channel=FRONT_WHEEL_CHANNEL):
		''' setup channels and basic stuff '''
		self.db = filedb.fileDB(db=db)
		self._channel = channel
		self._straight_angle = 90
		self.turning_max = 20
		self._turning_offset = int(self.db.get('turning_offset', default_value=0))

		self.wheel = Servo.Servo(self._channel, bus_number=bus_number, offset=self.turning_offset)
		self.debug = debug
		if self._DEBUG:
			print self._DEBUG_INFO, 'Front wheel PWM channel:', self._channel
			print self._DEBUG_INFO, 'Front wheel offset value:', self.turning_offset

		self._angle = {"left":self._min_angle, "straight":self._straight_angle, "right":self._max_angle}
		if self._DEBUG:
			print self._DEBUG_INFO, 'left angle: %s, straight angle: %s, right angle: %s' % (self._angle["left"], self._angle["straight"], self._angle["right"])

	def turn_left(self):
		''' Turn the front wheels left '''
		if self._DEBUG:
			print self._DEBUG_INFO, "Turn left"
		self.wheel.write(self._angle["left"])

	def turn_straight(self):
		''' Turn the front wheels back straight '''
		if self._DEBUG:
			print self._DEBUG_INFO, "Turn straight"
		self.wheel.write(self._angle["straight"])

	def turn_right(self):
		''' Turn the front wheels right '''
		if self._DEBUG:
			print self._DEBUG_INFO, "Turn right"
		self.wheel.write(self._angle["right"])

	def turn(self, angle):
		''' Turn the front wheels to the giving angle '''
		if self._DEBUG:
			print self._DEBUG_INFO, "Turn to", angle
		if angle < self._angle["left"]:
			angle = self._angle["left"]
		if angle > self._angle["right"]:
			angle = self._angle["right"]
		self.wheel.write(angle)

	@property
	def channel(self):
		return self._channel
	@channel.setter
	def channel(self, chn):
		self._channel = chn

	@property
	def turning_max(self):
		return self._turning_max

	@turning_max.setter
	def turning_max(self, angle):
		self._turning_max = angle
		self._min_angle = self._straight_angle - angle
		self._max_angle = self._straight_angle + angle
		self._angle = {"left":self._min_angle, "straight":self._straight_angle, "right":self._max_angle}

	@property
	def turning_offset(self):
		return self._turning_offset

	@turning_offset.setter
	def turning_offset(self, value):
		if not isinstance(value, int):
			raise TypeError('"turning_offset" must be "int"')
		self._turning_offset = value
		self.db.set('turning_offset', value)
		self.wheel.offset = value
		self.turn_straight()

	@property
	def debug(self):
		return self._DEBUG
	@debug.setter
	def debug(self, debug):
		''' Set if debug information shows '''
		if debug in (True, False):
			self._DEBUG = debug
		else:
			raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

		if self._DEBUG:
			print self._DEBUG_INFO, "Set debug on"
			print self._DEBUG_INFO, "Set wheel debug on"
			self.wheel.debug = True
		else:
			print self._DEBUG_INFO, "Set debug off"
			print self._DEBUG_INFO, "Set wheel debug off"
			self.wheel.debug = False

	def ready(self):
		''' Get the front wheels to the ready position. '''
		if self._DEBUG:
			print self._DEBUG_INFO, 'Turn to "Ready" position'
		self.wheel.offset = self.turning_offset
		self.turn_straight()

	def calibration(self):
		''' Get the front wheels to the calibration position. '''
		if self._DEBUG:
			print self._DEBUG_INFO, 'Turn to "Calibration" position'
		self.turn_straight()
		self.cali_turning_offset = self.turning_offset

	def cali_left(self):
		''' Calibrate the wheels to left '''
		self.cali_turning_offset -= 1
		self.wheel.offset = self.cali_turning_offset
		self.turn_straight()

	def cali_right(self):
		''' Calibrate the wheels to right '''
		self.cali_turning_offset += 1
		self.wheel.offset = self.cali_turning_offset
		self.turn_straight()

	def cali_ok(self):
		''' Save the calibration value '''
		self.turning_offset = self.cali_turning_offset
		self.db.set('turning_offset', self.turning_offset)

##########################################################################

def dpad(pos):
    if pos.bottom:

        back_wheels.forward()
        back_wheels.speed = DEFAULT_SPEED

    elif pos.top:
        back_wheels.backward()
        back_wheels.speed = DEFAULT_SPEED

    elif pos.left:
        front_wheels.turn_left()

    elif pos.right:
        front_wheels.turn_right()

    elif pos.middle:
        back_wheels.speed = 0
        front_wheels.turn_straight()


def main():
        bd = BlueDot()

        try:
                while True:
                        bd.wait_for_press()
                        bd.when_pressed = dpad
##                      bd.when_moved = dpad
                        bd.wait_for_release()


        except KeyboardInterrupt:
		print "KeyboardInterrupt, motor stop"
		back_wheels.stop()
	finally:
		print "Finished, motor stop"
		back_wheels.stop()
            

DEFAULT_SPEED = 70
back_wheels = Back_Wheels()
front_wheels = Front_Wheels()


if __name__ == '__main__':
    print "I'm running"
    main()
