from .analog import Analog

class Photoresistor(Analog):
    def __init__(self, GPIO_adc) -> None:
        super().__init__(GPIO_adc)
        
    