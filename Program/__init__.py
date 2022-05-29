import machine
import esp
from machine import Pin, ADC, Timer
import time
from .motors import Servo
from .photoresistor import Photoresistor

#GPIO
#photo_gpio = (34,35,32,33)
photo_gpio = { "RU":35, "LU":34,
               "RB":32, "LB":33 }
setup_btn_gpio = 25
motors_gpio = {'yaw':12, 'pitch':13} #yaw is rotate left and right, pitch is up and down

#varibles
duty_ranges = {'yaw':(40,120), 'pitch':(30,80)}

#objects
servos = {}
photo = {}

def setup():
    for k,v in motors_gpio.items():
        servos[k] = Servo(v, duty_range=duty_ranges[k])
    
    for k,v in photo_gpio.items():
        photo[k] = Photoresistor(v)

def loop():
    for i in range(100):
        for k,i in servos.items():
            try:
                i.duty +=1
            except:
                pass
            
        time.sleep(0.1)
    
    for k,i in photo.items():
            print(k,i.read())
        
    return 1

def fin():
    for k,i in servos.items():
        i.stop()

