import RPi.GPIO as GPIO
import time

class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose = False):
        self.gpio_pin = gpio_pin
        self.freq = pwm_frequency
        self.Dynamic_range = dynamic_range
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT, initial = 0)
        self.pwm = GPIO.PWM(self.gpio_pin, self.freq)
        self.pwm.start(0)

    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        self.pwm.stop()
        GPIO.output(self.gpio_pin, 0)
        GPIO.cleanup()

    def set_voltage(self, voltage):
        if  (0.0 <= voltage <= self.dynamic_range):
            pwm.ChangeDutyCycle(self.freq / self.dynamic_range * 100)
            duty_cycle = (voltage / self.dynamic_range * 100)
        else:
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} В)")
            print("Устанавливаем 0.0 В")
            return 0
        return(int(voltage / self.dynamic_range * 255))
            duty_cycle = 0
        self.pwm.ChangeDutyCycle(duty_cycle)
        print(f"Коэффициент заполнения {duty_cycle:.2f} B")

if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 500, 3.290, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вывведи не число. Попробуйте еще раз\n")
    finally: