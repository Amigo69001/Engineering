import RPi.GPIO as GPIO
import time

class R2R_ADC:
    
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False, 
                 comparator_high_when_v_in_gt_v_dac=True):
        """
        dynamic_range: максимальное измеряемое напряжение (В)
        compare_time: время ожидания после установки кода (сек)
        verbose: вывод отладочных сообщений
        comparator_high_when_v_in_gt_v_dac: 
            True  -> комп=1, когда V_in > V_dac
            False -> комп=1, когда V_dac > V_in
        """
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        # Сохраняем тип компаратора для использования в обоих методах
        self.comp_high_on_v_in_gt = comparator_high_when_v_in_gt_v_dac

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=GPIO.LOW)
        # Включаем подтяжку к земле (можно и к 3.3В, зависит от схемы)
        # Если компаратор с открытым коллектором — лучше pull-down
        GPIO.setup(self.comp_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # Небольшая задержка для стабилизации питания
        time.sleep(0.1)

    def number_to_dac(self, number):
        if self.verbose:
            print(f"Подача числа {number} на ЦАП")
        for i, pin in enumerate(self.bits_gpio):
            bit = (number >> i) & 1
            GPIO.output(pin, bit)

    def _comparator_trip(self):
        """Возвращает True, если компаратор сработал (условие 'V_in > V_dac' выполнено)"""
        value = GPIO.input(self.comp_gpio)
        if self.comp_high_on_v_in_gt:
            # Прямая логика: высокий уровень = V_in > V_dac
            return value == 1
        else:
            # Инверсная логика: низкий уровень = V_in > V_dac
            return value == 0

    def sequential_counting_adc(self):
        for code in range(256):
            self.number_to_dac(code)
            time.sleep(self.compare_time)
            if self._comparator_trip():
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

            # Если V_in > V_dac (компаратор сработал), то оставляем бит
            if self._comparator_trip():
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
        # Можно очистить все пины, но лучше только свои
        GPIO.cleanup(self.bits_gpio + [self.comp_gpio])
        if self.verbose:
            print("GPIO очищены")

    def __del__(self):
        if GPIO.getmode() is not None:  # избегаем ошибок при повторном вызове
            self.cleanup()


if __name__ == "__main__":
    DYNAMIC_RANGE = 3.30

    try:
        # Попробуйте изменить флаг, если результаты некорректны
        # comparator_high_when_v_in_gt_v_dac=False, если компаратор работает наоборот
        adc = R2R_ADC(dynamic_range=DYNAMIC_RANGE, 
                      compare_time=0.01, 
                      verbose=False,
                      comparator_high_when_v_in_gt_v_dac=True)
        print("Начинаем измерение напряжения методом SAR.")
        print("Для выхода нажмите Ctrl+C\n")

        while True:
            voltage = adc.get_sar_voltage()
            print(f"Напряжение (SAR): {voltage:.3f} В")
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nПрерывание пользователем")
    finally:
        if 'adc' in locals():
            adc.cleanup()   # убрана лишняя точка