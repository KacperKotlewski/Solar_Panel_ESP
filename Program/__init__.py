import machine
import esp
from machine import Pin, ADC, Timer
import time
from .motors import Servo

#GPIO
photo_gpio = (34,35,32,33)
setup_btn_gpio = 25
motors_gpio = {'yaw':12, 'pitch':13} #yaw is rotate left and right, pitch is up and down

#varibles
duty_ranges = {'yaw':(40,120), 'pitch':(30,80)}

#objects
servos = {}

def setup():
    global servos
    servos = {
        'yaw':Servo(motors_gpio['yaw'], duty_range=duty_ranges['yaw']), 
        'pitch':Servo(motors_gpio['pitch'], duty_range=duty_ranges['pitch'])
        }

def loop():
    for i in range(100):
        for k,i in servos.items():
            try:
                i.duty +=1
            except:
                pass
            
        time.sleep(0.1)

def fin():
    for k,i in servos.items():
        i.stop()

