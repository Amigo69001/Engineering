import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
leds = [16, 12, 25, 17, 27, 23, 22, 24]
GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds, 0)
button1 = 9
button2 = 10
GPIO.setup(button1, GPIO.IN)
GPIO.setup(button2, GPIO.IN)
num = 0
def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]
sleep_time = 0.2
while True:
    if GPIO.input(button1) and GPIO.input(button2):
        num = 255
        print(num, dec2bin(num))
        time.sleep(sleep_time)
    elif GPIO.input(button1):
        num = num + 1
        if num > 255:
            num = 0
        print(num, dec2bin(num))
        time.sleep(sleep_time)
    elif GPIO.input(button2):
        num = num - 1
        if num < 0:
            num = 255
        print(num, dec2bin(num))
        time.sleep(sleep_time)
    for i in range(len(leds)):
        GPIO.output(leds[i], dec2bin(num)[i])