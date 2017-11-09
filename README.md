# Automated_Plant_Watering
Raspberry Pi automated plant watering script

This is the main script for a automated Raspberry Pi water system. The
script loops through and checks the moisture every minute and logs it
in the subdirectory called 'Logs'. Every hour if the moisture is below a
certain threshold, then it will activate the motor to pump water into
the pot. There are two moisture sensors and two motors. The sensors on on the
back side of a MCP3008 transistor, and the motors are attached to GPIO port
numbers 17 and 27. The original script was written by Github user 'jerbly',
and modified by myself to use the motors for watering. If anyone has any
questions, feel free to email me at joejoejoey13@gmail.com. Enjoy!
