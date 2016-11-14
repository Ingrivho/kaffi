import RPi.GPIO as GPIO
import time

class Led():
    def __init__(self):
        self.pin = 22
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin,GPIO.OUT)

    def light_on(self):
        GPIO.output(self.pin, True)

    def light_off(self):
        GPIO.output(self.pin, False)

    def pulse(self, n, t):
        for n in range (0, n):
            self.light_on()
            time.sleep(t)
            self.light_off()
            time.sleep(t)
