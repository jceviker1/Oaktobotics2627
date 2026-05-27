import struct
import can
import time
import threading

#------------------------------------------------------------------------------------------------------------------
#
#
#----------------------ARBITRATION IDs-----------------------------------------------------------------------------
HEARTBEAT_ARBITRATION_ID = 0x2052C80 # Device Type: 2 (SparkMax) | Manufacturer: 5 (REV Robotics) | API Class: 11 | API Index: 2 | Device ID: 0 (broadcast to all devices)
BROADCAST_DISABLE_ARBITRATION_ID = 0x0000000 # Device Type: 0 (Device Broadcast) | Manufacturer: 0 (broadcast) | API Class: 0 | API Index: 0 | Device ID: 0 (broadcast to all devices)
BROADCAST_SYSTEM_HALT_ARBITRATION_ID = 0x0000040 # Device Type: 0 (Device Broadcast) | Manufacturer: 0 (broadcast) | API Class: 0 | API Index: 1 | Device ID: 0 (broadcast to all devices)

DUTY_CYCLE_SET_ARBITRATION_ID = 0x2050080 # Device Type: 2 (SparkMax) | Manufacturer: 5 (REV Robotics) | API Class: 0 | API Index: 2 | Device ID: 1-62
SPEED_SET_ARBITRATION_ID = 0x2050480 # Device Type: 2 (SparkMax) | Manufacturer: 5 (REV Robotics) | API Class: 1 | API Index: 2 | Device ID: 1-62
SMART_VELOCITY_SET_ARBITRATION_ID = 0x20504C0 # Device Type: 2 (SparkMax) | Manufacturer: 5 (REV Robotics) | API Class: 1 | API Index: 3 | Device ID: 1-62
POSITION_SET_ARBITRATION_ID = 0x2050C80 # Device Type: 2 (SparkMax) | Manufacturer: 5 (REV Robotics) | API Class: 3 | API Index: 2 | Device ID: 1-62
VOLTAGE_SET_ARBITRATION_ID = 0x2051080 # Device Type: 2 (SparkMax) | Manufacturer: 5 (REV Robotics) | API Class: 4 | API Index: 2 | Device ID: 1-62
CURRENT_SET_ARBITRATION_ID = 0x20510C0 # Device Type: 2 (SparkMax) | Manufacturer: 5 (REV Robotics) | API Class: 4 | API Index: 3 | Device ID: 1-62
SMART_MOTION_SET_ARBITRATION_ID = 0x2051480 # Device Type: 2 (SparkMax) | Manufacturer: 5 (REV Robotics) | API Class: 5 | API Index: 2 | Device ID: 1-62

STATUS_FRAME_0_ARBITRATION_ID = 0x2051800 # Device Type: 2 (SparkMax) | Manufacturer: 5 (REV Robotics) | API Class: 6 | API Index: 0 | Device ID: 0-62
STATUS_FRAME_1_ARBITRATION_ID = 0x2051840 # Device Type: 2 (SparkMax) | Manufacturer: 5 (REV Robotics) | API Class: 6 | API Index: 1 | Device ID: 0-62
STATUS_FRAME_2_ARBITRATION_ID = 0x2051880 # Device Type: 2 (SparkMax) | Manufacturer: 5 (REV Robotics) | API Class: 6 | API Index: 2 | Device ID: 0-62
STATUS_FRAME_3_ARBITRATION_ID = 0x20518C0 # Device Type: 2 (SparkMax) | Manufacturer: 5 (REV Robotics) | API Class: 6 | API Index: 3 | Device ID: 0-62
STATUS_FRAME_4_ARBITRATION_ID = 0x2051900 # Device Type: 2 (SparkMax) | Manufacturer: 5 (REV Robotics) | API Class: 6 | API Index: 4 | Device ID: 0-62
STATUS_FRAME_5_ARBITRATION_ID = 0x2051940 # Device Type: 2 (SparkMax) | Manufacturer: 5 (REV Robotics) | API Class: 6 | API Index: 5 | Device ID: 0-62
STATUS_FRAME_6_ARBITRATION_ID = 0x2051980 # Device Type: 2 (SparkMax) | Manufacturer: 5 (REV Robotics) | API Class: 6 | API Index: 6 | Device ID: 0-62


#-------------------CLASS DEFINITIONS------------------------------------------------------------------------------
class SparkMaxStatus:


    def __init__(self, deviceID, status_frames=None):
        self.deviceID = deviceID
        self.status_frames = [None]*7
        self.current = None
        self.voltage = None
        self.velocity = None
        self.temperature = None
        self.position = None
        self.ac_voltage = None
        self.analog_velocity = None
        self.analog_sensor_position = None
        self.alternate_encoder_velocity = None
        self.alternate_encoder_position = None

    def get_device_id(self):
        return self.deviceID
    
    def update_status_frame(self, Status_Frame_Index, new_status_frame):
        self.status_frames[Status_Frame_Index] = new_status_frame

    def get_status_frame(self, Status_Frame_Index):
        return self.status_frames[Status_Frame_Index]

    def get_frame_1(self):
        frame = self.get_status_frame(1)
        if frame is None:
            return None
        
        data = frame.data

        self.current = int(format(data[7], '08b') + format(data[6], '08b')[4:8], 2)/32.0
        self.voltage = int(format(data[6], '08b')[0:4] + format(data[5], '08b'), 2)/256.0
        self.velocity = struct.unpack('<f', bytes(data[0:4]))[0]
        self.temperature = int(format(data[4], '08b'), 2)
        self.update_status_frame(1, None)
        
        return (self.velocity, self.temperature, self.voltage, self.current)
    
    def get_frame_2(self):
        frame = self.get_status_frame(2)
        if frame is None:
            return None
        
        data = frame.data
        self.position = struct.unpack('<f', bytes(data[0:4]))[0]
        # Process data for frame 2
        self.update_status_frame(2, None)
        
        return self.position
    
    def get_frame_3(self):
        frame = self.get_status_frame(3)
        if frame is None:
            return None
        
        data = frame.data

        ac_voltage_raw = format(data[0], '08b') + format(data[1], '08b')[0:2]
        self.ac_voltage = int(ac_voltage_raw, 2) / 256.0


        analog_velocity_raw_bit = format(data[4], '08b')[7] + format(data[3], '08b') + format(data[2], '08b') + format(data[1], '08b')[2:8]
        analog_velocity_raw_int = int(analog_velocity_raw_bit, 2)

        # sign‑extend 23‑bit
        if analog_velocity_raw_int & (1 << 22):
            analog_velocity_raw_int -= (1 << 23)

        self.analog_velocity = analog_velocity_raw_int / 128.0

        self.analog_sensor_position = struct.unpack('<f', bytes([ (data[4] >> 1) & 0x7f] + list(data[5:8])))[0]
        # Process data for frame 3
        self.update_status_frame(3, None)
        
        return self.ac_voltage, self.analog_velocity, self.analog_sensor_position

    def get_frame_4(self):
        frame = self.get_status_frame(4)
        if frame is None:
            return None
        
        data = frame.data
        self.alternate_encoder_velocity = struct.unpack('<f', bytes(data[0:4]))[0]
        self.alternate_encoder_position = struct.unpack('<f', bytes(data[4:8]))[0]
        # Process data for frame 4
        self.update_status_frame(4, None)
        
        return self.alternate_encoder_velocity, self.alternate_encoder_position

    def get_frame_index(self, frame):
        return self.status_frames.index(frame)

    def get_current(self):
        return self.current
    def get_voltage(self):
        return self.voltage
    def get_velocity(self):
        return self.velocity
    def get_temperature(self):
        return self.temperature
    def get_position(self):
        return self.position
    def get_ac_voltage(self):
        return self.ac_voltage
    def get_analog_velocity(self):
        return self.analog_velocity
    def get_analog_sensor_position(self):
        return self.analog_sensor_position
    def get_alternate_encoder_velocity(self):
        return self.alternate_encoder_velocity
    def get_alternate_encoder_position(self):
        return self.alternate_encoder_position



# ------------------Global variables-------------------------------------------------------------------------------
bus = None
terminate = False
device_halt = False
bus_Message = None
thread_heartbeat = None
thread_Bus_Message = None
status_array = [SparkMaxStatus(i) for i in range(63)]

# ------------------Functions--------------------------------------------------------------------------------------

# Open CAN bus
def open_bus(interface='slcan', channel='COM5', bitrate=1000000):
    global bus, thread_heartbeat, thread_Bus_Message
    try:
        bus = can.Bus(interface=interface, channel=channel, bitrate=bitrate)
        print("CAN bus opened successfully")

        # Constant 10ms Heartbeat on a separate thread
        thread_heartbeat = threading.Thread(target=heartbeat, daemon=True)
        thread_heartbeat.start()
        thread_Bus_Message = threading.Thread(target=read_Can_Message, daemon=True)
        thread_Bus_Message.start()
        return True

    except Exception:
        print("Canable could not connect")
        return False

#Sends a heartbeat every 10ms by default
#Heartbeat - non-RIO
#0x2052C80 arbitration id || Device Type: 2 (SparkMax) | Manufacturer: 5 (REV Robotics) | API Class: 11 | API Index: 2 | Device ID: 0 (broadcast to all devices)
def heartbeat(heartbeat_ms_interval=10):
    while not terminate: # Unless terminate is set to True, send heartbeat on its thread
        heartbeat_msg = can.Message(
        arbitration_id=0x2052C80, # 32 bit extended arb id with leading 0s removed, 0x02052C80
        data=[0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff], # All 64bits set to 1
        is_extended_id=True # Sparkmax uses extended 29 bit arbitration IDs
        ) #Broadcast to all SparkMax controllers, id is set to 0 for broadcast
        try:
            bus.send(heartbeat_msg) # Send the heartbeat message
            time.sleep(heartbeat_ms_interval / 1000.0)
        except Exception:
            break




#Set the duty cycle of the motor controller, -1 >= value >= 1
def duty_cycle_set(value, index):
    value_IEEE = struct.pack('<f', value) # Convert the value to a IEEE 754 float ordered in little endian
    bus.send(can.Message(
        arbitration_id=0x2050080 + index & 0xFFFFFFFF, # 32 bit extended arb id; bc index is the last set of bits, index can be added to the arb id at device id 0
        data=list(value_IEEE) + [0x00,0x00,0x00,0x00], # send 32 bits of float data with the remaining 32 bits to fufill sparkmax's 64 bit data expectation
        is_extended_id=True
    ))

#Sets the target speed in RPM
def speed_set(value, index):
    value_IEEE = struct.pack('<f', value) # Convert the value to a IEEE 754 float ordered in little endian
    bus.send(can.Message(
        arbitration_id=SPEED_SET_ARBITRATION_ID + index, # 32 bit extended arb id; bc index is the last set of bits, index can be added to the arb id at device id 0
        data=list(value_IEEE) + [0x00,0x00,0x00,0x00], # send 32 bits of float data with the remaining 32 bits to fufill sparkmax's 64 bit data expectation
        is_extended_id=True
    ))

#Sets the target speed in RPM; respects max acceleration and velocity parameters
def smart_velocity_set(value, index):
    value_IEEE = struct.pack('<f', value) # Convert the value to a IEEE 754 float ordered in little endian
    bus.send(can.Message(
        arbitration_id=SMART_VELOCITY_SET_ARBITRATION_ID + index, # 32 bit extended arb id; bc index is the last set of bits, index can be added to the arb id at device id 0
        data=list(value_IEEE) + [0x00,0x00,0x00,0x00], # send 32 bits of float data with the remaining 32 bits to fufill sparkmax's 64 bit data expectation
        is_extended_id=True
    ))

#Sets the target position in revolutions
def position_set(value, index):
    value_IEEE = struct.pack('<f', value) # Convert the value to a IEEE 754 float ordered in little endian
    bus.send(can.Message(
        arbitration_id=POSITION_SET_ARBITRATION_ID + index, # 32 bit extended arb id; bc index is the last set of bits, index can be added to the arb id at device id 0
        data=list(value_IEEE) + [0x00,0x00,0x00,0x00], # send 32 bits of float data with the remaining 32 bits to fufill sparkmax's 64 bit data expectation
        is_extended_id=True
    ))

# Sets the target voltage in volts
def voltage_set(value, index):
    value_IEEE = struct.pack('<f', value) # Convert the value to a IEEE 754 float ordered in little endian
    bus.send(can.Message(
        arbitration_id=VOLTAGE_SET_ARBITRATION_ID + index, # 32 bit extended arb id; bc index is the last set of bits, index can be added to the arb id at device id 0
        data=list(value_IEEE) + [0x00,0x00,0x00,0x00], # send 32 bits of float data with the remaining 32 bits to fufill sparkmax's 64 bit data expectation
        is_extended_id=True
    ))

#Sets the target current in amperes
def current_set(value, index):
    value_IEEE = struct.pack('<f', value) # Convert the value to a IEEE 754 float ordered in little endian
    bus.send(can.Message(
        arbitration_id=CURRENT_SET_ARBITRATION_ID + index, # 32 bit extended arb id; bc index is the last set of bits, index can be added to the arb id at device id 0
        data=list(value_IEEE) + [0x00,0x00,0x00,0x00], # send 32 bits of float data with the remaining 32 bits to fufill sparkmax's 64 bit data expectation
        is_extended_id=True
    ))

#Sets the target position in revolutions? Maybe?
def smart_motion_set(value, index):
    value_IEEE = struct.pack('<f', value) # Convert the value to a IEEE 754 float ordered in little endian
    bus.send(can.Message(
        arbitration_id=SMART_MOTION_SET_ARBITRATION_ID + index, # 32 bit extended arb id; bc index is the last set of bits, index can be added to the arb id at device id 0
        data=list(value_IEEE) + [0x00,0x00,0x00,0x00], # send 32 bits of float data with the remaining 32 bits to fufill sparkmax's 64 bit data expectation
        is_extended_id=True
    ))

def manual_can_frame(value,arbitration_id, data):
    bus.send(can.Message(
        arbitration_id=arbitration_id,
        data=data, 
        is_extended_id=True
    ))

def read_Can_Message():
    while not terminate:
        
        try:
            global bus_Message, status_array
            #time.sleep(.01)
            bus_Message = bus.recv(timeout=1) # Wait for a message with a timeout of 1 second

            if bus_Message is not None:
                device_id = bus_Message.arbitration_id & 0x3F # Extract the device ID from the arbitration ID:
                if device_id == 0: # If the device ID is 0, it's a broadcast message, so we can ignore it for status frames
                    continue
                elif device_id < len(status_array):
                    if bus_Message.arbitration_id == (STATUS_FRAME_0_ARBITRATION_ID + device_id):
                        status_array[device_id].update_status_frame(0, bus_Message)
                    elif bus_Message.arbitration_id == (STATUS_FRAME_1_ARBITRATION_ID + device_id):
                        status_array[device_id].update_status_frame(1, bus_Message)
                    elif bus_Message.arbitration_id == (STATUS_FRAME_2_ARBITRATION_ID + device_id):
                        status_array[device_id].update_status_frame(2, bus_Message)
                    elif bus_Message.arbitration_id == (STATUS_FRAME_3_ARBITRATION_ID + device_id):
                        status_array[device_id].update_status_frame(3, bus_Message)
                    elif bus_Message.arbitration_id == (STATUS_FRAME_4_ARBITRATION_ID + device_id):
                        status_array[device_id].update_status_frame(4, bus_Message)
                    elif bus_Message.arbitration_id == (STATUS_FRAME_5_ARBITRATION_ID + device_id):
                        status_array[device_id].update_status_frame(5, bus_Message)
                    elif bus_Message.arbitration_id == (STATUS_FRAME_6_ARBITRATION_ID + device_id):
                        status_array[device_id].update_status_frame(6, bus_Message)



        except Exception as e:
            print(f"Error reading CAN message: {e}")
            return None




# close()
def close():
    global terminate, thread_heartbeat, thread_Bus_Message
    terminate = True

    #if thread_heartbeat is not None:
        #thread_heartbeat.join(timeout=2)
    #if thread_Bus_Message is not None:
        #thread_Bus_Message.join(timeout=2)
    time.sleep(1)

    try:
        bus.shutdown()  # Close CAN bus
    except Exception:
        pass
    print("Terminated SparkMax_Controller")
