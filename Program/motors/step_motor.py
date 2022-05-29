from . import Motor
from machine import Pin, PWM
import time

class Stepper(Motor):
    _duty = None
    _duty_range = (0,200)
    _freq = None
    _GPIO = None
    DEBUG = False
    
    def __init__(self, GPIO_step, GPIO_dir, GPIO_en = None) -> None:
        super().__init__()
        self.GPIO_step = GPIO_step
        self.GPIO_dir = GPIO_dir
        self.GPIO_en = GPIO_en
        self._steps = 0
        self._steps_to_make = 0
        self.last_step_time = 0
        self.speed_in_Hz = 100
        self._last_step_value = False
        
        self._setup_pin()
    
    
    @property
    def GPIO_step(self) -> int:
        return self._GPIO_step
    @GPIO_step.setter
    def GPIO_step(self, value) -> None:
        if isinstance(value, int):
            self._GPIO_step = value
            self._setup_pin()
        else:
            raise TypeError("Invalid GPIO_step")
        
    @property
    def GPIO_dir(self) -> int:
        return self._GPIO_dir
    
    @GPIO_dir.setter
    def GPIO_dir(self, value) -> None:
        if isinstance(value, int):
            self._GPIO_dir = value
            self._setup_pin()
        else:
            raise TypeError("Invalid GPIO_dir")
        
    @property
    def GPIO_en(self) -> int:
        return self._GPIO_en
    
    @GPIO_en.setter
    def GPIO_en(self, value) -> None:
        if isinstance(value, int):
            self._GPIO_en = value
            self.enable = True
        else:
            raise TypeError("Invalid GPIO_en")
        
    @property
    def enable(self) -> bool:
        return self._enable
    @enable.setter
    def enable(self, value) -> None:
        self._enable = value
        try:
            self._p_en = Pin(self.GPIO_en, mode=Pin.OUT, value=self._enable)
        except:
            print("enable pin not set")
    
    def _setup_pin(self) -> None:
        if self.GPIO_step is not None and self.GPIO_dir is not None:
            self._p_step = Pin(self.GPIO_step, mode=Pin.OUT)
            self._p_dir = Pin(self.GPIO_dir, mode=Pin.OUT)

    def stop(self) -> None:
        self.deinit()

    def deinit(self) -> None:
        pass
        
    def is_busy(self) -> bool:
        return self._steps_to_make != 0

    def step(self, step):
        self._steps_to_make = step
        self._continue_step()
    
    def _continue_step(self):
        if self.is_busy() and self._update_time():
            is_minus = self._steps_to_make < 0
            prefix = -1 if is_minus else 1
            
            self._steps += prefix*1
            self._steps_to_make -= prefix*1
            if self._steps >= self._steps_to_make:
                self._p_dir.value(is_minus)
                self._last_step_value != self._last_step_value
                self._p_step.value(self._last_step_value)
            
    def _update_time(self):
        t = time.ticks_ms()
        if t-self.last_step_time > 1/self.speed_in_Hz:
            self.last_step_time = t
            return True
        return False
    
    def update(self):
        if self.is_busy():
            self._continue_step()