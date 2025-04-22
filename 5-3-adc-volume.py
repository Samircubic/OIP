import RPi.GPIO as GPIO
import time
import sys

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

leds   = [2, 3, 4, 17, 27, 22, 10, 9]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(leds, GPIO.OUT)

def dec2bin(value):
    return [int(b) for b in format(value, '08b')]

def adc_simple():
    for i in range(256):
        GPIO.output(dac, dec2bin(i))
        time.sleep(0.001)
        if GPIO.input(comp):
            return i
    return 255

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

method = adc_sar if len(sys.argv) > 1 and sys.argv[1].lower() == "sar" else adc_simple

try:
    while True:
        num = method()
        voltage = num / 255 * 3.3
        leds_on = int(num * 8 / 256)
        signal = [1 if i < leds_on else 0 for i in range(8)]
        GPIO.output(leds, signal)
        print(f"ADC={num:3d}  V={voltage:.2f} V  LEDs={leds_on}")
        time.sleep(0.1)
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(troyka, GPIO.LOW)
    GPIO.output(leds, GPIO.LOW)
    GPIO.cleanup()
