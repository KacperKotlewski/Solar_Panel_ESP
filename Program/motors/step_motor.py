from . import Motor
from machine import Pin, PWM
import time
from ..timers import Timer, Time_calculations
from ..util import dprint

class Stepper(Motor):
    _GPIO_step = None
    _GPIO_dir = None
    _GPIO_en = None
    DEBUG = False
    
    def __init__(self, GPIO_step, GPIO_dir, GPIO_en = None, speed_in_Hz=10) -> None:
        super().__init__()
        self.GPIO_step = GPIO_step
        self.GPIO_dir = GPIO_dir
        self.GPIO_en = GPIO_en
        self._steps = 0
        self._steps_to_make = 0
        self.last_step_time = Timer()
        self.speed_in_Hz = speed_in_Hz
        self._last_step_value = 0
        
        self._setup_pin()
        
    def _setup_pin(self) -> None:
        dprint("_setup_pin","self.GPIO_step is not None",self.GPIO_step is not None)
        dprint("_setup_pin","self.GPIO_dir is not None",self.GPIO_dir is not None)
        if self.GPIO_step is not None and self.GPIO_dir is not None:
            self._p_step = Pin(self.GPIO_step, mode=Pin.OUT)
            self._p_dir = Pin(self.GPIO_dir, mode=Pin.OUT)
            dprint("_setup_pin","_p_step",self._p_step)
            dprint("_setup_pin","_p_dir",self._p_dir)
        
    def is_busy(self) -> bool:
        dprint("is_busy","_steps_to_make",self._steps_to_make)
        return self._steps_to_make != 0

    def step(self, step):
        dprint("step","step",step)
        self._steps_to_make = step
        self._continue_step()
    
    def _continue_step(self):
        if self.is_busy() and self._update_time():
            dprint("_continue_step","condition True")
            is_minus = self._steps_to_make < 0
            prefix = -1 if is_minus else 1
            dprint("_continue_step","prefix",prefix)
            self._steps += prefix*1
            self._steps_to_make -= prefix*1
            dprint("_continue_step","_steps",self._steps)
            dprint("_continue_step","_steps_to_make",self._steps_to_make)
            dprint("_continue_step","abs(self._steps) >= abs(self._steps_to_make)",abs(self._steps) >= abs(self._steps_to_make))
            if abs(self._steps_to_make):
                self._p_dir.value(1 if is_minus else 0)
                self._last_step_value = 0 if self._last_step_value == 1 else 1
                self._p_step.value(self._last_step_value)
                dprint("_continue_step","_p_dir",self._p_dir.value())
                dprint("_continue_step","_last_step_value",self._last_step_value)
                dprint("_continue_step","_p_step",self._p_step.value())
            
    def _update_time(self):
        dprint("_update_time","self.last_step_time.get_time().ms()",self.last_step_time.get_time().ms())
        dprint("_update_time","1/self.speed_in_Hz",1000/self.speed_in_Hz)
        dprint("_update_time","self.last_step_time.get_time().ms() > 1/self.speed_in_Hz",self.last_step_time.get_time().ms() > 1000/self.speed_in_Hz)
        if self.last_step_time.get_time().ms() > 1000/self.speed_in_Hz:
            self.last_step_time.reset()
            return True
        return False
    
    def update(self):
        dprint("is_busy","_steps_to_make",self._steps_to_make)
        if self.is_busy():
            self._continue_step()
            
    def stop(self):
        if self._steps != 0:
            self.step(-self._steps)
            self.update()
