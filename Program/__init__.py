import machine
import esp
from machine import Pin, ADC, Timer
import time
import motors

#GPIO
photo_gpio = (34,35,32,33)
setup_btn_gpio = 25
motors_gpio = {'yaw':12, 'pitch':13} #yaw is rotate left and right, pitch is up and down

#varibles
duty_ranges = {'yaw':(40,120), 'pitch':(30,80)}

#objects
servos = {}

def setup():
    servos = {
        'yaw':motors.Servo(motors_gpio['yaw'], duty_range=duty_ranges['yaw']), 
        'pitch':motors.Servo(motors_gpio['pitch'], duty_range=duty_ranges['pitch'])
        }

def loop():
    print("loop")

def fin():
    print("fin")