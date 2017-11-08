

import time, mcp3008, os
import RPi.GPIO as GPIO
from time import gmtime, strftime

'''
This test file allows someone to test the relays they hang off of 
GPIO ports 17 and 27. It allows to see if the relays turn one or not. 
Please do not have any devices connected to the relays unless
it is ok to test the relay connecting voltage through to any 
devices that are on the other side of the relay.
'''



# Sets the GPIO mode to BCM for calling on the pins
GPIO.setmode(GPIO.BCM)
# Sets the GPIO pins we are using (17 and 27) to an out pin
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)
GPIO.output(27, GPIO.HIGH)

time.sleep(15)

GPIO.output(17, GPIO.LOW)
time.sleep(5)
GPIO.output(17, GPIO.HIGH)

time.sleep(2)

GPIO.output(27, GPIO.LOW)
time.sleep(2)
GPIO.output(27, GPIO.HIGH)

