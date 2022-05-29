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
acc = 100 #accuracy of the photoresistor

#objects
servos = {}
photo = {}

#func
def step(servo, step):
    try:
        servo.duty +=step
    except:
        pass

#program
def setup():
    for k,v in motors_gpio.items():
        servos[k] = Servo(v, duty_range=duty_ranges[k])
    
    for k,v in photo_gpio.items():
        photo[k] = Photoresistor(v)

def loop():            
    #yaw
    for t in (('LU', 'RU'), ('LB','RB')):
        p0 = photo[t[0]].read()
        p1 = photo[t[1]].read()
        r = (p0  - p1 )//acc
        if r < 0:
            servos['yaw'].step(-1)
        elif r > 0:
            servos['yaw'].step(1)
        time.sleep(0.1)
         
    #pitch
    for t in (('LU', 'LB'), ('RU','RB')):
        p0 = photo[t[0]].read()
        p1 = photo[t[1]].read()
        r = (p0  - p1 )//acc
        if r > 0:
            servos['pitch'].step(-1)
        elif r < 0:
            servos['pitch'].step(1)
        time.sleep(0.1)
        
    #return 1

def fin():
    for k,i in servos.items():
        i.stop()


