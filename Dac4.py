import smbus
import time

class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=True):
        self.bus = smbus.SMBus(1)
        time.sleep(1)

        self.address = address
        self.wm = 0x00
        self.pds = 0x00

        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def deinit(self):
        self.bus.close()

    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")

        if not (0 <= number <= 4095):
            print("Число выходит на разрядность MCP4725 (12 бит)")

        first_byte = self.wm | self.pds | number >> 8
        second_byte = number & 0xFF
        self.bus.write_byte_data(0x61, first_byte, second_byte)

        if self.verbose:
            print(f"Число: {number}, отправленные по I2C данные:\
                [0x{(self.address << 1):02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]\n")
        
    def set_voltage(self, voltage):
        if (0 <= voltage <= self.dynamic_range):
            number = int(voltage / self.dynamic_range * 4095)
            self.set_number(number)
        else:
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} В)")


if __name__ == "__main__":
    try:
        mcp = MCP4725(5.11)

        while True:
            try:
                voltage = float(input("Введите напряжение в вольтах: "))
                mcp = mcp.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз")
    finally:
        mcp.deinit()