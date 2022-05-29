import machine
import esp
from machine import Pin, ADC, Timer
import time
from .motors import Servo, Stepper
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
photo = {}
servos = {}

#func
def calc_photo_diff(p0, p1):
    return (p0  - p1 )//acc

def move_to_light(motor, pair_of_photo, dire=1):
    p = pair_of_photo
    r = calc_photo_diff(photo[p[0]].read(), photo[p[1]].read())
    motor.step(dire*r)
    
def servo_loop():
    for t in (('LU', 'RU'), ('LB','RB')):
        move_to_light(servos['yaw'],t)
        time.sleep(0.1)
         
    for t in (('LU', 'LB'), ('RU','RB')):
        move_to_light(servos['pitch'],t, -1)
        time.sleep(0.1)
    
def step_loop():
    for t in (('LU', 'RU'), ('LB','RB')):
        move_to_light(servos['yaw'],t)
        time.sleep(0.1)
         
    for t in (('LU', 'LB'), ('RU','RB')):
        move_to_light(servos['pitch'],t, -1)
        time.sleep(0.1)


#program
def setup():
    for k,v in photo_gpio.items():
        photo[k] = Photoresistor(v)
        
    for k,v in motors_gpio.items():
        servos[k] = Servo(v, duty_range=duty_ranges[k])

def loop():
    servo_loop()
    #return 1

def fin():
    for k,i in servos.items():
        i.stop()


