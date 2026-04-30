import pwm_dac
import signal_generator as sg
import time

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000

try:
    dac = pwm_dac.PWM_DAC(12, 500, 3.290)
    while True:
        t = time.time()
        norm = sg.get_sin_wave_amplitude(signal_frequency, t)
        voltage = norm * amplitude
        dac.set_voltage(voltage)
        sg.wait_for_sampling_period(sampling_frequency)
finally:
    dac.deinit()