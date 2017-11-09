"""
This is the main script for a automated Raspberry Pi water system. The 
script loops through and checks the moisture every minute and logs it
in the subdirectory called 'Logs'. Every hour if the moisture is below a 
certain threshold, then it will activate the motor to pump water into
the pot. There are two moisture sensors and two motors. The sensors on on the 
back side of a MCP3008 transistor, and the motors are attached to GPIO port
numbers 17 and 27. The original script was written by Github user 'jerbly',
and modified by myself to use the motors for watering. If anyone has any 
questions, feel free to email me at joejoejoey13@gmail.com. Enjoy!
"""

import time, mcp3008, os, logging
import RPi.GPIO as GPIO
from time import gmtime, strftime

# ANSI escape codes
PREVIOUS_LINE="\x1b[1F"
RED_BACK="\x1b[41;37m"
GREEN_BACK="\x1b[42;30m"
YELLOW_BACK="\x1b[43;30m"
RESET="\x1b[0m"

# Sets the GPIO mode to BCM for calling on the pins
GPIO.setmode(GPIO.BCM)
# Sets the GPIO pins we are using (17 and 27) to an out pin
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)
GPIO.output(27, GPIO.HIGH)

# Sets the logging mode for the logging module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# creates a file handler
log_num = 1
handler = logging.FileHandler('./Logs/Moisture_log'+str(log_num)+'.txt')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

# Main definition that handles the sensors and hourly watering
def hourly_checks():
	print '\x1b[2J\x1b[H'
	print 'Moiture sensor'
	print '==============\n'
	global PREVIOUS_LINE, RED_BACK, GREEN_BACK, YELLOW_BACK, RESET, \
	title_screen, log_num
	# Main loop
	while True:
		# Calls on definition 'get_avg' which will get an average of
		# 10 sensor readings
		m = get_avg(5)
		m2 = get_avg(6)
		# Checks for over sized log files and sets a new file if it's too large
		statinfo = os.stat('./Logs/Moisture_log'+str(log_num)+'.txt')
		file_size = statinfo.st_size
		# If the log file is larger than 1MB, increment the log_num
		# var in order to make a new log file
		if int(file_size) > 1000:
			log_num = log_num + 1
			handler = logging.FileHandler('./Logs/Moisture_log' \
			+str(log_num)+'.txt')
		# Threshold checks on the moisture sensors
		if m < 310:
			# Sets the background according to the mooisture 
			# level of the mango sensor and prints it
			background = RED_BACK
			print PREVIOUS_LINE + background + "Mango moisture"+ \
			" level: {:>5} ".format(m) + RESET
			# If the garlic sensor is too dry then it will 
			# activate the motor for ten seconds and record in 
			# the log it was watered this hour
			logger.info('Hourly - Mango sensor: Moisture '+ \
			'level: '+str(m)+' - Watered this hour. \n')
			GPIO.output(17, GPIO.LOW)
			time.sleep(3)
			GPIO.output(17, GPIO.HIGH)
		else: 
			# Sets the background color according to the 
			#moisture level of the mango sensor and prints it
			background = GREEN_BACK
			print PREVIOUS_LINE + background + "Mango moisture"+ \
			" level: {:>5} ".format(m) + RESET
			logger.info('Hourly - Mango sensor: Moiture level: '+ \
			str(m)+'.\n')
		# If the garlic sensor is too dry then it will activate the 
		# motor for ten seconds and record in the log it was 
		# watered this hour
		if m2 < 350:
			print ("Garlic moisture level: {:>5} ".format(m2))
			logger.info('Hourly - Garlic sensor: Moisture '+ \
			'level: '+str(m2)+' - Watered this hour. \n')
			GPIO.output(27, GPIO.LOW)
			time.sleep(2)
			GPIO.output(27, GPIO.HIGH)
		# If the moisture sensor wasn't too dry, it will just log 
		#the readings
		else:
			print ("Garlic moisture level: {:>5} ".format(m2))
			logger.info('Hourly - Garlic sensor: Moiture '+ \
			'level: '+str(m2)+'.\n')

#		f.close()
		# Waits until next watering cycle
		watering_cycle()

def get_avg(sensor):
	# Saves 10 readings from the moisture sensor, then takes
	# the average and saves it as variable 'm'
	readings = []
	num_readings = 10
	while num_readings > 0:
		# Get current moisture readings
		m = mcp3008.readadc(sensor)
		# Save 
		readings.append(m)
		num_readings = num_readings - 1
	m = sum(readings)/len(readings)
	return m

# Definition to display readings between watering cycles
def watering_cycle():
	minutes = 60
	# Loop that happens for one hour and logs readings every minute
	while minutes > 0:
		# Get the moisture readings
		m = get_avg(5)
		m2 = get_avg(6)
		# Log the new moisture sensor for the minute
		logger.info('Minute check - Mango sensor: Moiture level: '+ \
		str(m)+'.\n')
		logger.info('Minute check - Garlic sensor: Moiture level: '+ \
		str(m2)+'.\n')
		# Wait for one minute before going through the loop again
		time.sleep(60)
		# Takes one away from the varibale "minutes" to track 
		# when the hourly cycle can end and return
		minutes = minutes - 1

if __name__ == "__main__":
	while True:
		try:
			hourly_checks()
		except (SystemExit, KeyboardInterrupt):
			raise
		except Exception as e:
			global log_num
			logger.error('Failed at keeping the plants '+ \
			'watered...', exc_info=True)
