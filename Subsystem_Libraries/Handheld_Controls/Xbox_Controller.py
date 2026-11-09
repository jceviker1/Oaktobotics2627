# Avi's controller code

'''
    To use:
    1. use setUpController() to set up the controller (outside the loop)
    2. use getInput(controller) to get the controller input (inside the loop)
        ljh, ljv, rjh, rjv, lt, rt, A, B, X, Y, lb, rb, back, start, ljb, rjb, dpl, dpr, dpu, dpd = Xbox_Controller.getInput(controller)
    3. profit
'''
import pygame
import numpy as np

controller = None
PRINT_DELAY = 0.1 #gives a delay between prints

Trigger_Deadzone = 0.1 #lil deadzone for the triggers
    
def deadzone(value, Deadzone=Trigger_Deadzone):
    if abs(value) < Deadzone:
        return 0
    else:
        return value

def normalizeTrigger(value, Deadzone=Trigger_Deadzone):
    #-1 means that trigger is not pressed in pygame, so we need to make it 0
    normalized = (value + 1.0) / 2.0 
    normalized = np.clip(normalized, 0, 1)
    normalized = deadzone(normalized, Deadzone)
    return normalized

def setUpController():
    global controller
    pygame.init()
    pygame.joystick.init()

    controller = pygame.joystick.Joystick(0)
    controller.init()

    return controller

def getInput(controller, Deadzone=Trigger_Deadzone):
    pygame.event.pump() #this updates controller input

    ljh = deadzone(controller.get_axis(0), Deadzone)   # left joystick horizontal
    ljv = deadzone(controller.get_axis(1), Deadzone)   # left joystick vertical
    rjh = deadzone(controller.get_axis(2), Deadzone)   # right joystick horizontal
    rjv = deadzone(controller.get_axis(3), Deadzone)   # right joystick vertical
    lt = normalizeTrigger(controller.get_axis(4), Deadzone)     # left trigger
    rt = normalizeTrigger(controller.get_axis(5), Deadzone)     # right trigger

    # buttons are 0 or 1 so they don't need deadzones
    A = controller.get_button(0)
    B = controller.get_button(1)
    X = controller.get_button(2)
    Y = controller.get_button(3)
    lb = controller.get_button(4) # left bumper
    rb = controller.get_button(5) # right bumper
    back = controller.get_button(6)
    start = controller.get_button(7)
    ljb = controller.get_button(8) # left joystick pressing button
    rjb = controller.get_button(9) # right joystick pressing button
    # the Xbox button is get_button(10), but it opens the Xbox menu so we're not using it

    if controller.get_hat(0)[0] == -1:  # D-pad left
        dpl = 1
    else:
        dpl = 0
    if controller.get_hat(0)[0] == 1:  # D-pad right
        dpr = 1
    else:
        dpr = 0
    if controller.get_hat(0)[1] == 1: # D-pad up
        dpu = 1
    else:
        dpu = 0
    if controller.get_hat(0)[1] == -1: # D-pad down
        dpd = 1
    else:
        dpd = 0

    return ljh, ljv, rjh, rjv, lt, rt, A, B, X, Y, lb, rb, back, start, ljb, rjb, dpl, dpr, dpu, dpd

# These functions are the same as getInput, but they only return the inputs you need

def getTriggers(controller, Deadzone=Trigger_Deadzone):
    ljh, ljv, rjh, rjv, lt, rt, A, B, X, Y, lb, rb, back, start, ljb, rjb, dpl, dpr, dpu, dpd = getInput(controller, Deadzone)
    return lt, rt
    
def getButtons(controller, Deadzone=Trigger_Deadzone):
    ljh, ljv, rjh, rjv, lt, rt, A, B, X, Y, lb, rb, back, start, ljb, rjb, dpl, dpr, dpu, dpd = getInput(controller, Deadzone)
    return A, B, X, Y, lb, rb, back, start, ljb, rjb, dpl, dpr, dpu, dpd

def getJoysticks(controller, Deadzone=Trigger_Deadzone):
    ljh, ljv, rjh, rjv, lt, rt, A, B, X, Y, lb, rb, back, start, ljb, rjb, dpl, dpr, dpu, dpd = getInput(controller, Deadzone)
    return ljh, ljv, rjh, rjv

def getDPad(controller, Deadzone=Trigger_Deadzone):
    ljh, ljv, rjh, rjv, lt, rt, A, B, X, Y, lb, rb, back, start, ljb, rjb, dpl, dpr, dpu, dpd = getInput(controller, Deadzone)
    return dpl, dpr, dpu, dpd





