#!/usr/bin/python3

import wiringpi 
import time

# http://wiringpi.com/reference/core-functions/

led = 26

wiringpi.wiringPiSetupGpio() 	# GPIO (BCM) numbering

wiringpi.pinMode(led, 1)	# BCM26 as OUTPUT

for i in range(10):
	print ("LED OFF")
	wiringpi.digitalWrite(led, 0)
	time.sleep(2)
	print ("LED ON")
	wiringpi.digitalWrite(led, 1)
	time.sleep(2)

