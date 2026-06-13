#andrijas controller code
import pygame
import time

controller = None
PRINT_DELAY = 0.1 #gives a delay between prints

Trigger_Deadzone = 0.1 #lil deadzone for the triggers

#this makes it so that the values are between -1 and 1
#so the thing doesnt break if like it goes past it for some reason
def clamp(value, min_value, max_value):
    if(value < min_value):
        return min_value
    elif(value > max_value):
        return max_value
    else:
        return value
    
def deadzone(value):
    if abs(value) < Trigger_Deadzone:
        return 0
    else:
        return value

def normalizeTrigger(value):
    #-1 means that trigger is not pressed in pygame, so we need to make it 0
    normalized = (value + 1.0) / 2.0 
    normalized = clamp(normalized, 0, 1)
    normalized = deadzone(normalized)
    return normalized

def normalizeJoystick(value):
    #joystick is already between -1 and 1 but we want a deadzone
    normalized = clamp(value, -1, 1)
    normalized = deadzone(normalized)
    return normalized

def setUpController():
    global controller
    pygame.init()
    pygame.joystick.init()

    controller = pygame.joystick.Joystick(0)
    controller.init()

    return controller

def getDriveInput(controller):
    pygame.event.pump() #this updates controller input

    #its probably 4 and 5 but change it if it isnt
    left_trigger_raw = controller.get_axis(4)
    right_trigger_raw = controller.get_axis(5)

    arm_input = controller.get_axis(1)
    bucket_input = controller.get_axis(3)

    left_trigger = normalizeTrigger(left_trigger_raw)
    right_trigger = normalizeTrigger(right_trigger_raw)

    arm_input = normalizeJoystick(arm_input)
    bucket_input = normalizeJoystick(bucket_input)

    #bumpers to make it negative
    left_bumper = controller.get_button(4)
    right_bumper = controller.get_button(5)

    #returns negative if bumper pressed
    if left_bumper:
        if left_trigger > 0:
            left_wheels = -left_trigger
        else:
            left_wheels = 0
    else:
        left_wheels = left_trigger

    if right_bumper:
        if right_trigger > 0:
            right_wheels = -right_trigger
        else:
            right_wheels = 0
    else:
        right_wheels = right_trigger

    return left_wheels, right_wheels, arm_input, bucket_input