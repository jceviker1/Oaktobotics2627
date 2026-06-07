import SparkMax_Controller
import time
import controller

SparkMax_Controller.open_bus(channel="COM5")
remote = controller.setUpController()

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

        SparkMax_Controller.status_array[2].update_data()
        SparkMax_Controller.status_array[3].update_data()
        SparkMax_Controller.status_array[4].update_data()
        curr3 = SparkMax_Controller.status_array[3].get_voltage()
        curr2 = SparkMax_Controller.status_array[2].get_voltage()
        curr4 = SparkMax_Controller.status_array[4].get_voltage()
        print("curr3:", curr3, "curr2:", curr2, "curr4:", curr4)
        try:
            print("total_current =" + str(curr3 + curr2 + curr4))
        except:
            print("Error occurred while calculating total current")
        time.sleep(.05)

except KeyboardInterrupt:
    SparkMax_Controller.close()



