from machine import Pin, ADC

class Analog:
    def __init__(self, GPIO_adc) -> None:
        self._GPIO = GPIO_adc
        self._adc = ADC(Pin(self._GPIO))
        self._value = self._adc.read()
        
    def read(self):
        self._value = self._adc.read()
        return self._value
        
    