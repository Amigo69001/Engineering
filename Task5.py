import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)

state = 0


p_transistor = 6
GPIO.setup (p_transistor, GPIO.IN)

while True:
    state = not GPIO.input (p_transistor)
    GPIO.output (led, state)