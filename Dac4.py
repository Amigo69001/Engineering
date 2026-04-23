import smbus

class set_U_num():
    def __init__(self, dynamic_range, adress = 0x61, verbose = True):
        self.bus = smbus.SMBus(1)

        self.adress = adress
        self.vm  = 0x00
        self.pds = 0x00

        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def set_number(self, number):
        if (number > 0xFFF):
            print("num out of range")
            return 0
        fb = self.vm | self.pds | number >> 8
        sb = number & 0xFF

        self.bus.write_byte_data(self.adress, fb, sb)

        if self.verbose:
            print(f"adress: {self.adress}\n\tfb = 0x{fb:02x}\n\tsb = 0x{sb:02x}\n")

    def put_U(self, U):
        number = int(0xFFF * U / self.dynamic_range)
        self.set_number(number)

    def deinit(self):
        self.bus.close()

if __name__ == "__main__":
    dac = set_U_num(5.284)

    try:
        while 1:
            try:
                U = float(input("Введите напряжение в Вольтах:"))
                dac.put_U(U)
            except ValueError:
                print("это не число")
    finally:
        dac.deinit()