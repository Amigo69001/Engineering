
from matplotlib import pyplot as plt
import RPi.GPIO as gpio
import time


dynamic_range = 3.304


class R2R_DAC():
    def __init__(self, dynamic_range, comporator_time, verbose = False):
        self.gpio_bits = [26,20,19,16,13,12,25,11][::-1]
        self.comp_gpio = 21
        self.vlt_arr = [0]
        self.time_arr = [0]

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
        timer = 0

        num = 255
        del_num = 128

        for i in range (8):
            self.lights(num)
            if gpio.input(self.comp_gpio):
                num -= del_num
                del_num //= 2

            time.sleep(0.02)
            timer += 0.02

        return timer, self.num_to_voltage(num)
    
    def destroy(self):
        gpio.output(self.gpio_bits, 0)
        gpio.cleanup()

    def show_U_arr(self, time_max):

        while self.time_arr[-1] < time_max:
            timer, U = self.put_U()
            self.time_arr.append(self.time_arr[-1]+timer)
            self.vlt_arr.append(U)

        print(len(self.time_arr))

        plt.figure(figsize=(10,6))
        plt.plot(self.time_arr[1:], self.vlt_arr[1:])

        plt.show()

check_U = R2R_DAC(dynamic_range, 0.1)
check_U.show_U_arr(3)
check_U.destroy()