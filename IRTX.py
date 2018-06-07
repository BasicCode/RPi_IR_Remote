#! /bin/python
# RPi based IR transmitter

import sys
import time
import pigpio
import signal

#Handle ctrl-C, no longer used because program ends naturally.
def sigint_handler(signum, frame):
	#Clean up on SIGTERM
	pi.hardware_PWM(pwm_pin, 0, 0)
	pi.write(data_pin, 0)
	pi.stop()
	print("Bye")
	sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

#Wave form
#approx. 500us pulse width
pulse_width = 0.000375

#The PWM pin at 38khz will be modulated by the data pin
pwm_pin = 18
data_pin = 17
pi = pigpio.pi()

#The desired data stream. Manually read off the oscilloscope screen
data_stream = [0b10111101, 0b11111111, 0b01111101, 0b01101101, 0b01011100]

#Sends each bit in the data stream individually. MSB first.
def sendData():
	for byte in data_stream:
		for i in range(7, -1, -1):
			pi.write(data_pin, (byte >> i) & 0x01)
			time.sleep(pulse_width)
			pi.write(data_pin, 0)
			time.sleep(pulse_width)

#this is just a starting sequence that the remote uses
def startBit():
	#3200us start bit
	pi.write(data_pin, 1)
	time.sleep(.0032)
	#LOW for at least 9600us
	pi.write(data_pin, 0)
	time.sleep(0.0096)

#Try to clean up the mess. Not working!
def stop():
	pi.hardware_PWM(pwm_pin, 0, 0)
	pi.write(data_pin, 0)
	pi.stop()
	print("Done!")

if __name__ == "__main__":
	#Start the PWM which will be modulated by the data
	pi.hardware_PWM(pwm_pin, 38000, 500000)
	#Start bit sequence
	startBit()
	#Send the dat
	sendData()
	#Clean up
	stop()
