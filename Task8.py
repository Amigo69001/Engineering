import time
import RPi.GPIO as GPIO

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

GPIO.setmode(GPIO.BCM)

leds = [16, 12, 25, 17, 27, 23, 22, 24]
GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds, 0)

UP_BTN = 9
DOWN_BTN = 10
GPIO.setup(UP_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DOWN_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

num = 0

sleep_time = 0.2


while True:
    up = GPIO.input(UP_BTN)
    down = GPIO.input(DOWN_BTN)
  
    if up and down:
        num = 255
        #print(num, dec2bin(num))
        time.sleep(sleep_time)

    elif up:
        num += 1
        if num > 255:
            num = 0
        #print(num, dec2bin(num))
        time.sleep(sleep_time)

    elif down:
        num -= 1
        if num < 0:
            num = 0
        #print(num, dec2bin(num))
        time.sleep(sleep_time)

    GPIO.output(leds, dec2bin(num))