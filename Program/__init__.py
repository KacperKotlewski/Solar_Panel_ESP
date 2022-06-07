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
import uasincio 
#from .web_server import *

#GPIO
#photo_gpio = (34,35,32,33)
photo_gpio = { "RU":35, "LU":34,
               "RB":33, "LB":32 }
setup_btn_gpio = 25
motor_gpio = None #you can define it here or below, it depent from you
motors_servo_gpio = {'yaw':12, 'pitch':13} #yaw is rotate left and right, pitch is up and down
motors_step_gpio = {'yaw':(21,19), 'pitch':(18,5)} #yaw is rotate left and right, pitch is up and down
stepers_enable = 23

stops = (12,14,27,26)

#varibles
duty_ranges = {'yaw':(40,120), 'pitch':(30,80)} #for servos
acc = 100 #accuracy of the photoresistor
finish_flag = False
stepper_move_flag = True

#select what you use
types_of_motor = {0:"stepper", 1:"servo"}
motor_type = types_of_motor[0]

#objects
photo = {}
motors = {}
timers = {}}

btn = Better_Button(pin=setup_btn_gpio, pull = Pin.PULL_UP)
stoppers = (Button(pin=pin, pull = Pin.PULL_DOWN) for pin in stops)

if motor_type == types_of_motor[0]:
    steppers_en = Pin(stepers_enable, mode=Pin.OUT)

#event callbacks
def callback(*args):
    print("dummy callback", *args)
    
def close():
    global finish_flag
    finish_flag = True

def motor_on_after_period():
    turn_on_motors()
    timers['motors_sleep'].deinit()
    timers['motors_sleep'] = None



#eventy

#func
    
def calc_photo_diff(p0, p1):
    return (p0  - p1 )//acc

def move_to_light(motor, pair_of_photo, dire=1):
    p = pair_of_photo
    r = calc_photo_diff(photo[p[0]].read(), photo[p[1]].read())
    motor.step(dire*r)

def move_motor_by_photo(motor, photoresistor_setup=(('LU', 'RU'), ('LB','RB')), direction=1):
    if motor.is_busy():
        motor.update()
        return
    for t in photoresistor_setup:
        move_to_light(motor, t, direction)
            
def motor_loop():
    if stepper_move_flag == False:
        return
    move_motor_by_photo(motors['yaw'],   (('LU', 'RU'), ('LB','RB')), direction=-1)
    move_motor_by_photo(motors['pitch'], (('LU', 'LB'), ('RU','RB')), direction=-1)
    if motor_type == types_of_motor[1]:
        time.sleep(0.1)

def turn_motors(on):
    if steppers_en != None:
        steppers_en.value = 1 if not on else 0
        stepper_move_flag = on

turn_off_motors = lambda : turn_motors(on=False)
turn_on_motors  = lambda : turn_motors(on=True)


#async func
async def should_i_turn_off_motors():
    diff = [calc_photo_diff(pair) for pair in (('LU', 'RU'), ('LB','RB'), 'LU', 'LB'), ('RU','RB'))]
    if all([i<=1 for i in diff]):
        turn_off_motors()
        period = 10*60*1000 #10 min
        t = Timer()
        t.init(mode=Timer.ONE_SHOT, period=period, callback=motor_on_after_period)
        timers['motors_sleep'] = t

        await uasyncio.sleep_ms(period)
    await uasyncio.sleep_ms(500)


#program
def setup():
    if DEBUG:
        for i in range(100):
            print("")
        print("-"*100)
        print("initialazing stuff")
        print("-"*100)
        
    for k,v in photo_gpio.items():
        photo[k] = Photoresistor(v)
        
    global motor_gpio
    if motor_type == types_of_motor[0]:
        if motor_gpio is None:
            motor_gpio = motors_step_gpio
        for k,v in motor_gpio.items():
            motors[k] = Stepper(v[0], v[1], speed_in_Hz=500)
        
    elif motor_type == types_of_motor[1]:
        if motor_gpio is None:
            motor_gpio = motors_servo_gpio
        for k,v in motor_gpio.items():
            motors[k] = Servo(v, duty_range=duty_ranges[k])
        
        
    
    #btn.add_on_press(Event(switch_move_flag))
    #btn.add_on_relase(Event(callback, "relase"))
    #btn.add_on_series(2, Event(callback, "double click"))
    btn.add_after_long_press(5, Event(close))
    for b in stoppers:
        b.add_on_press(Event(close))
    
    #start_server()
     
last_dir = -1
def loop():
    return uasyncio.run(async_loop())

async def async_loop():
    dprint("loop")

    btn.check()

    await should_i_turn_off_motors()
    motor_loop()
    
    
    if DEBUG:
        time.sleep(0.2)
    if finish_flag:
        return 1
    

def fin():
    mot = [i for k,i in motors.items()]
    true_table = [m.is_busy() for m in mot] + [True]
    while any(true_table):
        if DEBUG:
            time.sleep(0.2)
        for i in mot:
            i.stop()
        if any(true_table):
            true_table = [m.is_busy() for m in mot] + [False]


