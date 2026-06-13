import SparkMax_Controller
import time
import controller
import DataToCSV

SparkMax_Controller.open_bus(channel="COM5")
remote = controller.setUpController()
DataToCSV.HeaderWrite()
def skid_steer(left, right):

    SparkMax_Controller.duty_cycle_set(left_wheels,1)
    SparkMax_Controller.duty_cycle_set(left_wheels,4)
    SparkMax_Controller.duty_cycle_set(-right_wheels,3)
    SparkMax_Controller.duty_cycle_set(-right_wheels,2)


try:
    while True:
        left_wheels, right_wheels, arm_input, bucket_input = controller.getDriveInput(remote)
        skid_steer(left_wheels, right_wheels)
        print("left:", left_wheels, "right:", right_wheels, "arm:", -arm_input, "bucket:", bucket_input)
        DataToCSV.DataToCSV(1)
        DataToCSV.DataToCSV(2)
        DataToCSV.DataToCSV(3)
        DataToCSV.DataToCSV(4)


        time.sleep(.05)

except KeyboardInterrupt:
    SparkMax_Controller.close()



