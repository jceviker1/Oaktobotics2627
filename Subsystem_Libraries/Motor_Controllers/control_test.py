import struct
import can
import time
import threading
import SparkMax_Controller as smc
import random
import pygame

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

smc.open_bus(channel='COM3')

while True:
    pygame.event.pump()
    pos = 0.1 *joystick.get_axis(1) # -1 to 1
    smc.duty_cycle_set(pos, 3) # -1 to 1
    print(str(smc.status_array[3].get_frame_1()))
    time.sleep(0.1)


smc.close()
