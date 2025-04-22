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

def adc():
    for value in range(256):
        signal = dec2bin(value)
        GPIO.output(dac, signal)
        time.sleep(0.03)
        comp_value = GPIO.input(comp)
        if comp_value == 1:
            return value
    return 255

try:
    while True:
        digital_value = adc()
        voltage = digital_value / 255.0 * 3.3
        print(f"Digital value: {digital_value}, Voltage: {voltage:.2f} V")
finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()
