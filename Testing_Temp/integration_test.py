# written by Avi to test integrating everything
# Last updated in early October I think
from Subsystem_Libraries.Motor_Controllers import SparkMax_Controller as smc
from Subsystem_Libraries.Socket_Testing import Coms
from Subsystem_Libraries.Handheld_Controls import Controller
import time

# Open the bus. COM3 is the serial port for the canable and varies by computer
smc.open_bus(interface='slcan', channel='COM3', bitrate=1000000)
device_id = 3  # the CAN ID configured on the SparkMax (should be on the sparkmax)

# Set up the controller
controller = Controller.setUpController()
print("Program started. Left trigger controls motor speed. Press the right trigger to exit.")

while True:
    # Get the drive input from the controller
    left_wheels, right_wheels, arm_input, bucket_input = Controller.getDriveInput(controller)

    # Use the left trigger to control the motor speed (0.3 is to reduce speed)
    smc.duty_cycle_set((0.3 * left_wheels), device_id)

    if right_wheels > 0.5:  # if right trigger is pressed more than halfway, end program
        print("Right trigger pressed, breaking loop")
        break

    time.sleep(0.1)  # small delay to avoid overwhelming the bus

# clean up
smc.duty_cycle_set(0.0, device_id)  # Ensure the motor is stopped
smc.close() # Close the bus
print("Program terminated.")