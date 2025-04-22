import RPi.GPIO as GPIO
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return [int(bit) for bit in format(value, '08b')]

def adc_sar():
    value = 0
    for value in range(256):
        signal = dec2bin(value)
        GPIO.output(dac, signal)
        time.sleep(0.03)
        comp_value = GPIO.input(comp)
        if comp_value == 1:
            return value
    return value

try:
    while True:
        t0 = time.perf_counter()
        num = adc_sar()
        t1 = time.perf_counter()
        voltage = num / 255 * 3.3
        dt_ms = (t1 - t0) * 1e3
        print(f"SAR ADC → {num:3d} | {voltage:.2f} V | time: {dt_ms:.1f} ms")
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(troyka, GPIO.LOW)
    GPIO.cleanup()
