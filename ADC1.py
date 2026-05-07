import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.1, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        a = [int(i) for i in bin(number)[2:].zfill(8)]
        for i in range(len(a)):
            GPIO.output(self.bits_gpio[i], a[i])

    def sequential_counting_adc(self):
        for dac_value in range(256):
            self.number_to_dac(dac_value)
            time.sleep(0.01)
            time.sleep(0.0001)
            comparator_output = GPIO.input(self.comp_gpio)
            if comparator_output == 1:
                return dac_value
        return 255

    def get_sc_voltage(self):
        digital_value = self.sequential_counting_adc()
        voltage = (digital_value / 255) * self.dynamic_range
        return voltage

if __name__ == "__main__":
    try:
        r2r_adc = R2R_ADC(3.3)
        while True:
            voltage = r2r_adc.get_sc_voltage()
            print(f'Напряжение: {voltage} В')
    finally: