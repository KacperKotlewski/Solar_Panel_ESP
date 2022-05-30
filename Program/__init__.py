import machine
import esp
from machine import Pin, ADC, Timer
import time
from .motors import Servo, Stepper
from .photoresistor import Photoresistor
from .button import Button, Better_Button
from .event import Event
from .util import dprint
from .settings import DEBUG

#GPIO
#photo_gpio = (34,35,32,33)
photo_gpio = { "RU":35, "LU":34,
               "RB":32, "LB":33 }
setup_btn_gpio = 25
motors_gpio = {'yaw':12, 'pitch':13} #yaw is rotate left and right, pitch is up and down
motors_step_gpio = {'yaw':(22,1), 'pitch':(3,21)} #yaw is rotate left and right, pitch is up and down
stepers_enable = 23

#varibles
duty_ranges = {'yaw':(40,120), 'pitch':(30,80)}
acc = 100 #accuracy of the photoresistor
finish_flag = False

#objects
photo = {}
servos = {}
steps = {}
steppers_en = Pin(stepers_enable, mode=Pin.OUT)
btn = Better_Button(pin=setup_btn_gpio, pull = Pin.PULL_UP)

#event callbacks
def callback(*args):
    print("dummy callback", *args)
    
def close(*args):
    global finish_flag
    finish_flag = True

#eventy

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
        
        
def is_step_free(step):
    step.update()
    return not step.is_busy()
    
def step_loop():
    s = steps['yaw']
    if is_step_free(s):
        for t in (('LU', 'RU'), ('LB','RB')):
            move_to_light(s,t)
         
    s = steps['pitch']
    if is_step_free(s):
        for t in (('LU', 'RU'), ('LB','RB')):
            move_to_light(s,t)


#program
def setup():
    for k,v in photo_gpio.items():
        photo[k] = Photoresistor(v)
        
    for k,v in motors_gpio.items():
        servos[k] = Servo(v, duty_range=duty_ranges[k])
        
    #for k,v in motors_step_gpio.items():
        #steps[k] = Stepper(v[0], v[1])
        
    
    #steppers_en.value(0)
    #btn.add_on_press(Event(callback, "press"))
    #btn.add_on_relase(Event(callback, "relase"))
    #btn.add_on_series(2, Event(callback, "double click"))
    btn.add_after_long_press(5, Event(close))
     

def loop():
    dprint("loop")
    btn.check()
    
    servo_loop()
    
    if DEBUG:
        time.sleep(0.3)
    if finish_flag:
        return 1
    

def fin():
    for k,i in servos.items():
        i.stop()

