

import mcp3008

'''
This test file takes readings off moisture sensors from channels 5 and 6
on the back side of a MCP3008.
'''

# Definition to get the average of 10 sensor readings
def get_avg(sensor):
        # Saves 10 readings from the moisture sensor, then takes
        # the average and saves it as variable 'm'
        readings = []
        num_readings = 10
        while num_readings > 0:
                # Get current moisture readings from module in mcp2008 file
                m = mcp3008.readadc(sensor)
                # Save
                readings.append(m)
                num_readings = num_readings - 1
        m = sum(readings)/len(readings)
        return m

# Save the sensor readings
m = get_avg(5)
m2 = get_avg(6)

# Print the sensor readings
print("Mango sensor is at: "+str(m)) 
print("Garlic sensor is at: "+str(m2))

