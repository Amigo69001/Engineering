import RPi.GPIO as GPIO
import time

class R2R_ADC:
    
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
    
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]

        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=GPIO.LOW)
        # Исправление: добавляем встроенную подтяжку вверх для пина компаратора
        GPIO.setup(self.comp_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def number_to_dac(self, number):
        
        if self.verbose:
            print(f"Подача числа {number} на ЦАП")
        for i, pin in enumerate(self.bits_gpio):
            bit = (number >> i) & 1
            GPIO.output(pin, bit)

    def sequential_counting_adc(self):
       
        for code in range(256):
            self.number_to_dac(code)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio) == 1:
                if self.verbose:
                    print(f"Превышение достигнуто при коде {code}")
                return code
        return 255

    def get_sc_voltage(self):
        
        code = self.sequential_counting_adc()
        voltage = code * self.dynamic_range / 255.0
        if self.verbose:
            print(f"[SC] Код: {code}, напряжение: {voltage:.3f} В")
        return voltage

    def successive_approximation_adc(self):
        
        code = 0
        for bit in range(7, -1, -1):
            test_code = code | (1 << bit)
            self.number_to_dac(test_code)
            time.sleep(self.compare_time)

            if GPIO.input(self.comp_gpio) == 0:
                code = test_code

        if self.verbose:
            print(f"[SAR] Найден код: {code}")
        return code

    def get_sar_voltage(self):
        code = self.successive_approximation_adc()
        voltage = code * self.dynamic_range / 255.0
        if self.verbose:
            print(f"[SAR] Код: {code}, напряжение: {voltage:.3f} В")
        return voltage

    def cleanup(self):
        self.number_to_dac(0)
        GPIO.cleanup(self.bits_gpio + [self.comp_gpio])
        if self.verbose:
            print("GPIO очищены")

    def __del__(self):
        self.cleanup()


if __name__ == "__main__":
    DYNAMIC_RANGE = 3.30

    try:
        adc = R2R_ADC(dynamic_range=DYNAMIC_RANGE, compare_time=0.01, verbose=False)
        print("Начинаем измерение напряжения методом последовательного приближения (SAR).")
        print("Для выхода нажмите Ctrl+C\n")

        while True:
            voltage = adc.get_sar_voltage()
            print(f"Напряжение (SAR): {voltage:.3f} В")
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nПрерывание пользователем")

    finally:
        if 'adc' in locals():
            adc.cleanup()