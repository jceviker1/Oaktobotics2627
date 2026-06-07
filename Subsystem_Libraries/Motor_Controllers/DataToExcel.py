import csv
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import SparkMax_Controller as smc

print(smc.__file__)
print(os.getcwd())

# Define these
collecting = True       # set to False to stop logging
SparkMax1 = 'SparkMax1'
SparkMax2 = 'SparkMax2'
SparkMax3 = 'SparkMax3'
SparkMax4 = 'SparkMax4'

# Write headers
with open('MotorDataLog1.csv', 'w', newline='') as f:
    csv.writer(f).writerow(['Device ID', 'Velocity', 'Temperature', 'Voltage', 'Current', 'Position', 'AC Voltage', 'Analog Velocity', 'Analog Sensor Position', 'Alternate Encoder Velocity', 'Alternate Encoder Position'])
with open('MotorDataLog2.csv', 'w', newline='') as f:
    csv.writer(f).writerow(['Device ID', 'Velocity', 'Temperature', 'Voltage', 'Current', 'Position', 'AC Voltage', 'Analog Velocity', 'Analog Sensor Position', 'Alternate Encoder Velocity', 'Alternate Encoder Position'])
with open('MotorDataLog3.csv', 'w', newline='') as f:
    csv.writer(f).writerow(['Device ID', 'Velocity', 'Temperature', 'Voltage', 'Current', 'Position', 'AC Voltage', 'Analog Velocity', 'Analog Sensor Position', 'Alternate Encoder Velocity', 'Alternate Encoder Position'])
with open('MotorDataLog4.csv', 'w', newline='') as f:
    csv.writer(f).writerow(['Device ID', 'Velocity', 'Temperature', 'Voltage', 'Current', 'Position', 'AC Voltage', 'Analog Velocity', 'Analog Sensor Position', 'Alternate Encoder Velocity', 'Alternate Encoder Position'])

try:
    while collecting:
        for device_id in range(1, 5):  # iterates 1, 2, 3, 4
            with open(f'MotorDataLog{device_id}.csv', 'a', newline='') as f:
                csv.writer(f).writerow([
                    f'SparkMax{device_id}',
                    smc.status_array[device_id].velocity,
                    smc.status_array[device_id].temperature,
                    smc.status_array[device_id].voltage,
                    smc.status_array[device_id].current,
                    smc.status_array[device_id].position,
                    smc.status_array[device_id].ac_voltage,
                    smc.status_array[device_id].analog_velocity,
                    smc.status_array[device_id].analog_sensor_position,
                    smc.status_array[device_id].alternate_encoder_velocity,
                    smc.status_array[device_id].alternate_encoder_position
                ])
        time.sleep(0.01)  # 10ms between reads

except KeyboardInterrupt:
    smc.close()
    print("Logging stopped")