from machine import Pin
import time
from .event import EventManager, Event
from .timers import Timer, Time_calculations
from .util import dprint

class Button:
    def __init__(self, pin, pull = Pin.PULL_DOWN):
        self._btn = Pin(pin, Pin.IN, pull)
        self._press_value = 0 if pull == Pin.PULL_UP else 1
        self.press_timer = Timer()
        self.relase_timer = Timer()
        
        self.events = EventManager()
        
        self._type_of_action = {"inactive": 0, "pressed": 1, "released": 2}
        self._last_actions = [0, 0, 0]
        
    def is_pressed(self):
        return self._btn.value() == self._press_value
    
    def add_on_press(self, event):
        self.events.add_event("on_press", event)
        
    def add_on_relase(self, event):
        self.events.add_event("on_release", event)
        
    def _add_last_action(self, last):
        self._last_actions = [last]+self._last_actions[:2]
        
    def _if_is_pressed(self):
        pass
        
    def _if_is_released(self):
        pass
    
    def _on_press(self):
        self.press_timer.reset()
        
    def _on_relase(self):
        self.relase_timer.reset()
        
    def check(self):
        is_p = self.is_pressed()
        last = self._last_actions
        types = self._type_of_action
        dprint(type(self),self,"check", is_p)
        if is_p:
            dprint(type(self),self,"pressed")
            self._if_is_pressed()
            if last[0] != types["pressed"]:
                dprint(type(self),self,"First press signal")
                self._on_press()
                self.events.trigger_event("on_press")
                self._add_last_action(types["pressed"])
        else:
            dprint(type(self),self,"released")
            self._if_is_released()
            if last[0] != types["released"]:
                dprint(type(self),self,"First release signal")
                self._on_relase()
                self.events.trigger_event("on_release")
                self._add_last_action(types["released"])
                
                
    def time_of_pressing(self):
        if self.is_pressed():
            return self.press_timer.get_time()
        else:
            return Time_calculations(time.ticks_diff(self.press_timer._start_time, self.relase_timer._start_time))
        
    def time_between_pressing(self):
        return self.press_timer.get_time()
            
    
    def __call__(self):
        self.check()
        
class Better_Button(Button):
    def __init__(self, pin, pull = Pin.PULL_DOWN):
        super().__init__(pin, pull)
        self._series_click_counter = 0
        self._series_end_flag = False
        
    def __call__(self):
        self.check()
        
    def get_series(self):
        return self._series_click_counter, self._series_end_flag
        
    def _click_series(self):
        if self.relase_timer.get_time().sec() < 0.5:
            if self.time_between_pressing().sec() < 1:
                if self._series_end_flag:
                    self._series_click_counter = 0
                    self._series_end_flag = False
                self._series_click_counter += 1
                
    def _reset_flag(self):
        if self.relase_timer.get_time().sec() > 0.5:
            if self.time_between_pressing().sec() > 1:
                self._on_series()
                self._series_end_flag = True
                
    def _if_is_released(self):
        super()._if_is_released()
        self._reset_flag()
        
    def _on_press(self):
        super()._on_press()
        self._click_series()
        
    def _if_is_pressed(self):
        super()._if_is_pressed()
        self._on_long_press()
        
    def add_on_series(self, count_of_click, event):
        self.events.add_event("on_series"+str(count_of_click), event)
        
    def _on_series(self):
        self.events.trigger_event("on_series"+str(self._series_click_counter+1))
        
    def add_on_long_press(self, time_of_press_in_sec, event:Event):
        event_flag = [True]
        def on_long_press(btn:Button, time_of_press:float, event:Event, flag:list=list(tuple([True]))):
            if btn.time_of_pressing().sec() > time_of_press_in_sec:
                if flag[0]:
                    flag[0] = False
                    event()
            else:
                flag[0] = True
        event = Event(on_long_press, self, time_of_press_in_sec, event, event_flag)
        self.events.add_event("on_long_press", event)
        
    def _on_long_press(self):
        self.events.trigger_event("on_long_press")
