class Event:
    def __init__(self, callback=None, name=None, args=None):
        self.name = name
        self.callback = callback
        self.args = args
        
    def __call__(self):
        self.callback(self.args)
        
    def __str__(self):
        return self.name +"_"+ str(self.callback)
        
class EventManager:
    def __init__(self):
        self.events = {}
    
    def add_event(self, event_name, event:Event):
        if event_name not in self.events:
            self.events[event_name] = []
        self.events[event_name].append(event)
        
    def trigger_event(self, event_name):
        if event_name in self.events:
            for event in self.events[event_name]:
                event()
        
    def remove_event(self, event_name, event:Event):
        if event_name in self.events:
            self.events[event_name].remove(event)
        
    def remove_event_by_name(self, event_name, name):
        if event_name in self.events:
            for event in self.events[event_name]:
                if event.name == name:
                    self.events[event_name].remove(event)
                    break
        
    def remove_event_by_callback(self, event_name, callback):
        if event_name in self.events:
            for event in self.events[event_name]:
                if event.callback == callback:
                    self.events[event_name].remove(event)
                    break
    
                
    def remove_all_events(self, event_name):
        if event_name in self.events:
            self.events[event_name] = []
            
    def remove_all_events_from_callback(self, callback):
        for event_name in self.events:
            self.remove_event(event_name, callback)