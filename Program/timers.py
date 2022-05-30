import time

class Time_calculations(object):
    def __init__(self, ticks_ms):
        self.ticks_ms = ticks_ms
        
    def get(self):
        return self.ticks_ms   
        
    def ms(self):
        return self.get()    
    
    def sec(self):
        return self.ms() // 1000
    
    def min(self):
        return self.sec() // 60
    
    def hour(self):
        return self.min() // 60
    
    def day(self):
        return self.hour() // 24
    
    def week(self):
        return self.day() // 7
    
    def __str__(self):
        return str(self.get())
    def __repr__(self):
        return 'Time_calculations(%s)' % self.get()
    
    

class Timer:
    def __init__(self, start=True):
        self._last_time = 0
        self._start_time = 0
        if start:
            self.start()
        
    def start(self):
        self._start_time = time.ticks_ms()
    
    def stop(self):
        self.reset()
        
    @property
    def start_time(self):
        return Time_calculations(self._start_time)
    @property
    def last_time(self):
        return Time_calculations(self._last_time)
        
    
    def reset(self):
        self._last_time = self._start_time
        self._start_time = time.ticks_ms()
        
    def get_time(self):
        return Time_calculations(time.ticks_diff(time.ticks_ms(), self._start_time))
    
    def get_delta(self):
        return Time_calculations(time.ticks_diff(self._last_time, self._start_time))
