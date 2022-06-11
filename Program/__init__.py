import machine
import esp
from machine import Pin, ADC, Timer
import time
from .motors import Servo, Stepper
from .analog import Analog
from .photoresistor import Photoresistor
from .button import Button, Better_Button
from .event import Event
from .util import dprint
from .settings import DEBUG
import uasyncio 
from .web_server import *

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
battery_pin = 15
solar_pin = 0


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
timers = {}

btn = Better_Button(pin=setup_btn_gpio, pull = Pin.PULL_UP)
stoppers = (Button(pin=pin, pull = Pin.PULL_DOWN) for pin in stops)
bat = Analog(pin=battery_pin)
sol = Analog(pin=solar_pin)

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
        return
    for t in photoresistor_setup:
        move_to_light(motor, t, direction)
            
async def motor_loop():
    while True:
        if stepper_move_flag == False:
            await uasyncio.sleep(2)
            continue
        move_motor_by_photo(motors['yaw'],   (('LU', 'RU'), ('LB','RB')), direction=-1)
        move_motor_by_photo(motors['pitch'], (('LU', 'LB'), ('RU','RB')), direction=-1)
        if motor_type == types_of_motor[1]:
            await uasyncio.sleep(0.1)
        await uasyncio.sleep_ms(50)

def turn_motors(on):
    if steppers_en != None:
        steppers_en.value( 1 if not on else 0)
        stepper_move_flag = on

turn_off_motors = lambda : turn_motors(on=False)
turn_on_motors  = lambda : turn_motors(on=True)

def is_panel_centered():
    pairs = (('LU', 'RU'), ('LB','RB'), ('LU', 'LB'), ('RU','RB'))
    reads = [ [photo[i].read() for i in pair] for pair in  pairs]
    diff = [calc_photo_diff(pair[0], pair[1]) for pair in reads]
    return all([i<=1 for i in diff])


#async func
async def should_i_turn_off_motors():
    while True:
        if not stepper_move_flag:
            await uasyncio.sleep(5)
            continue

        if is_panel_centered():
            await uasyncio.sleep_ms(500)
        if is_panel_centered(): # sprawdza czy przez 0.5 min jest dobrze wyśrodkowane
            turn_off_motors()
            period = 30 *60*1000 #x min
            t = Timer()
            t.init(mode=Timer.ONE_SHOT, period=period, callback=motor_on_after_period)
            timers['motors_sleep'] = t

            await uasyncio.sleep_ms(period)
        await uasyncio.sleep_ms(500)
        

        
def charging_status():
    return False
        
def v_div(v,ro, r1=10000):
    return (v*ro)/(ro+r1)

def read_battery_status():
    value = v_div(bat.read(), 3300)  /12.4*100
    return round(value, 1)

def read_solar_status():
    value = v_div(bat.read(), 2100)
    return round(value, 1)
    
    

@app.route("/photoresistors", methods=["GET"])
async def API_ph(request):
    return Response({k:o.read() for k,o in photo.items()})

@app.route("/motors", methods=["GET"])
async def API_motor_move(request):
    return Response({k:o.is_busy() for k,o in motors.items()})

@app.route("/battery", methods=["GET"])
async def API_battery(request):
    return Response({"power":read_battery_status(), "status":charging_status()})

@app.route("/panel", methods=["GET"])
async def API_panel(request):
    return Response([read_solar_status()])



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
    dprint("loop")
    return uasyncio.run(async_loop())

async def async_loop():
    for k,m in motors.items():
        uasyncio.create_task(m.async_update_loop())
    uasyncio.create_task(should_i_turn_off_motors())
    uasyncio.create_task(motor_loop())
    uasyncio.create_task(start_server())
    while True:

        btn.check()
        
        
        if DEBUG:
            time.sleep(0.2)
        if finish_flag:
            return 1
        await uasyncio.sleep_ms(10)
    

def fin():
    mot = [i for k,i in motors.items()]
    for i in mot:
        i.stop()
    # true_table = [m.is_busy() for m in mot] + [True]
    # while any(true_table):
    #     if DEBUG:
    #         time.sleep(0.2)
    #     for i in mot:
    #         i.stop()
    #     if any(true_table):
    #         true_table = [m.is_busy() for m in mot] + [False]



