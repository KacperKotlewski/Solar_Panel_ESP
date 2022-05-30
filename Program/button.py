from machine import Pin
import time
from .event import EventManager, Event
from .timers import Timer, Time_calculations
from .util import dprint
from .settings import time_between_multi_presses, time_from_last_relase

print(time_between_multi_presses, time_from_last_relase)

class Button:
    def __init__(self, pin, pull = Pin.PULL_DOWN):
        self._btn = Pin(pin, Pin.IN, pull)
        self._press_value = 0 if pull == Pin.PULL_UP else 1
        self.press_timer = Timer()
        self.relase_timer = Timer()
        
        self.events = EventManager()
        
        self._type_of_action = {"inactive": 0, "pressed": 1, "released": 2}
        self._last_actions = [2,2,2]
        
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
            if last[0] != types["pressed"]:
                dprint(type(self),self,"First press signal")
                self._on_press()
                self.events.trigger_event("on_press")
                self._add_last_action(types["pressed"])
            self._if_is_pressed()
        else:
            dprint(type(self),self,"released")
            if last[0] != types["released"]:
                dprint(type(self),self,"First release signal")
                self._on_relase()
                self.events.trigger_event("on_release")
                self._add_last_action(types["released"])
            self._if_is_released()
                
                
    def time_of_pressing(self):
        if self.is_pressed():
            return self.press_timer.get_time()
        else:
            return Time_calculations(abs(time.ticks_diff(self.press_timer._start_time, self.relase_timer._start_time)))
        
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
    
    def is_series_still_running(self):
        return self._series_end_flag
        
    def _click_series(self):
        if self.relase_timer.get_time().sec() < time_from_last_relase:
            if self.time_between_pressing().sec() < time_between_multi_presses:
                if self._series_end_flag:
                    self._series_end_flag = False
                self._series_click_counter += 1
        else:
            self._series_click_counter = 1
        dprint(type(self),self,"count of click (",self._series_click_counter, "), end_flag (", self._series_end_flag,")")
                
    def _reset_flag(self):
        if self.relase_timer.get_time().sec() > time_from_last_relase:
            if self.time_between_pressing().sec() > time_between_multi_presses:
                self._on_series()
                self._series_end_flag = True
                
    def _if_is_released(self):
        super()._if_is_released()
        self._reset_flag()
        self._on_series()
        
    def _on_press(self):
        super()._on_press()
        self._click_series()
        self._on_series()
        
    def _if_is_pressed(self):
        super()._if_is_pressed()
        #self._on_long_press()
        self._on_series()
           
    def _on_relase(self):
        super()._on_relase()
        self._after_long_press()
        
    def add_on_series(self, count_of_click, event):
        def on_long_press(btn:Button, count_of_click:int, event:Event, flag:list=list(tuple([True]))):
            if btn._series_click_counter == count_of_click and btn.is_series_still_running():
                if flag[0]:
                    flag[0] = False
                    event()
            else:
                flag[0] = True
        event = Event(on_long_press, self, count_of_click, event)
        self.events.add_event("on_series", event)
        
    def _on_series(self):
        self.events.trigger_event("on_series")
        
    def add_after_long_press(self, time_of_press_in_sec, event:Event):
        def after_long_press(btn:Button, time_of_press:float, event:Event, flag:list=list(tuple([True]))):
            if btn.time_of_pressing().sec() > time_of_press_in_sec:
                if flag[0]:
                    flag[0] = False
                    event()
            else:
                flag[0] = True
        event = Event(after_long_press, self, time_of_press_in_sec, event)
        self.events.add_event("after_long_press", event)
        
    def _after_long_press(self):
        self.events.trigger_event("after_long_press")
