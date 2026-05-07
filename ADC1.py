import RPi.GPIO as gpio
import time

dynamic_range = 3.304


class R2R_DAC():
    def __init__(self, dynamic_range, comporator_time, verbose = False):
        self.gpio_bits = [26,20,19,16,13,12,25,11][::-1]
        self.comp_gpio = 21

        self.comporator_time = comporator_time
        self.dynamic_range   = dynamic_range
        self.verbose         = verbose

        gpio.setmode(gpio.BCM)

        gpio.setup(self.gpio_bits, gpio.OUT, initial = 0)
        gpio.setup(self.comp_gpio, gpio.IN)

    def num_to_voltage(self, num):
        if not (0 < num < 256):
            return 0
        return self.dynamic_range * num / 255

    def lights(self, num):
        for out in self.gpio_bits:
            gpio.output(out,num % 2)
            num //= 2
        return
    
    def put_U(self):
        num = 0
        self.lights(num)

        while (not gpio.input(self.comp_gpio)) and num < 256:
            num += 1
            self.lights(num)
            time.sleep(0.01)

        print(f"Напряжение: {self.num_to_voltage(num - 1):2f}V")
    
    def destroy(self):
        gpio.output(self.gpio_bits, 0)
        gpio.cleanup()

try:
    check_U = R2R_DAC(dynamic_range, 0.1)
    while 1:
        try:
            check_U.put_U()
        except ValueError:
            print("это не число")
        

finally:
    check_U.destroy()