import machine
import esp
from machine import Pin, ADC, Timer
import time

#GPIO
photo_gpio = (34,35,32,33)
setup_btn_gpio = 25
motors_gpio = {'yaw':12, 'pitch':13} #yaw is rotate left and right, pitch is up and down


def setup():
    print("setup")

def loop():
    print("loop")

def fin():
    print("fin")