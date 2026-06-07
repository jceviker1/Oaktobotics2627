



import csv
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import SparkMax_Controller as smc

def HeaderWrite():
    with open('MotorDataLog1.csv', 'w', newline='') as f:
        csv.writer(f).writerow(['Device ID', 'Velocity', 'Temperature', 'Voltage', 'Current', 'Position', 'AC Voltage', 'Analog Velocity', 'Analog Sensor Position', 'Alternate Encoder Velocity', 'Alternate Encoder Position'])
    with open('MotorDataLog2.csv', 'w', newline='') as f:
        csv.writer(f).writerow(['Device ID', 'Velocity', 'Temperature', 'Voltage', 'Current', 'Position', 'AC Voltage', 'Analog Velocity', 'Analog Sensor Position', 'Alternate Encoder Velocity', 'Alternate Encoder Position'])
    with open('MotorDataLog3.csv', 'w', newline='') as f:
        csv.writer(f).writerow(['Device ID', 'Velocity', 'Temperature', 'Voltage', 'Current', 'Position', 'AC Voltage', 'Analog Velocity', 'Analog Sensor Position', 'Alternate Encoder Velocity', 'Alternate Encoder Position'])
    with open('MotorDataLog4.csv', 'w', newline='') as f:
        csv.writer(f).writerow(['Device ID', 'Velocity', 'Temperature', 'Voltage', 'Current', 'Position', 'AC Voltage', 'Analog Velocity', 'Analog Sensor Position', 'Alternate Encoder Velocity', 'Alternate Encoder Position'])




def DataToCSV(device_id):
    
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
        
        time.sleep(0.5)  # 1/2s between reads
        


