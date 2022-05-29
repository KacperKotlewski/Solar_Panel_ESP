from motor import Motor
from machine import Pin, ADC, PWM

class Servo(Motor):
    def __init__(self, GPIO_pwm, pwm_freq=50, duty_range=(40,120)) -> None:
        super().__init__()
        self.GPIO = GPIO_pwm
        self.freq = pwm_freq
        self.duty_range = duty_range
        
        self.angle_to_servo_duty = lambda angle: int((self.duty_range[1] - self.duty_range[0]) * angle / 180) + self.duty_range[0]
        
        
        self._duty = self.duty_range[0]
        self._setup_pin()
        
        
        
    @property
    def duty_range(self) -> tuple:
        return self._duty_range
    
    @duty_range.setter
    def duty_range(self, value) -> None:
        if isinstance(value, [list, tuple]) and value.length > 2 and isinstance(value[0], int) and isinstance(value[1], int) and value[0] > 0 and value[1] >= value[0]:
            self._duty_range = tuple(value)
            self._check_duty_in_range()
        else:
            raise ValueError("Invalid duty_range range, type must be 'list' or 'tuple', also 'value[0]' must be greater than 0 and 'value[1]' must be greater than or equal to 'value[0]'")
        
    @property
    def duty(self) -> int:
        return self._duty
    
    @duty.setter
    def duty(self, value) -> None:
        if isinstance(value, int) and value >= self._duty_range[0] and value <= self._duty_range[1]:
            self._duty = value
            try:
                self._pwm.duty(self._duty)
            except:
                print("pwm not set")
        else:
            raise ValueError("Invalid duty, value must be in range of 'duty_range'")
        
    @property
    def GPIO(self) -> int:
        return self._GPIO
    
    @GPIO.setter
    def GPIO(self, value) -> None:
        if isinstance(value, int):
            self._GPIO = value
            self._setup_pin()
        else:
            raise TypeError("Invalid GPIO")
        
    @property
    def freq(self) -> int:
        return self._freq
    
    @freq.setter
    def freq(self, value) -> None:
        if isinstance(value, int):
            self._freq = value
            self._setup_pin()
        else:
            raise TypeError("Invalid freq")
    
    def _setup_pin(self) -> None:
        p = Pin(self.GPIO)
        self._pin = p
        self._pwm = PWM(p, freq=self.freq)
        self._pwm.duty(self._duty)
        
    def _check_duty_in_range(self) -> None:
        if self.duty < self.duty_range[0]:
            self.duty = self.duty_range[0]
        elif self.duty > self.duty_range[1]:
            self.duty = self.duty_range[1]
    
        
    def set_angle(self, angle) -> None:
        self._angle = angle
        self.duty(self.angle_to_servo_duty(angle))
        
    def set_duty(self, duty) -> None:
        self.duty(duty)