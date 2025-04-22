import RPi.GPIO as GPIO

GPIO.setwarnings(False)

dac = [6, 12, 5, 0, 1, 7, 11, 8]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

def dec2bin(num):
    return [int(bit) for bit in bin(num)[2:].zfill(8)]

try:
    while True:
        num = input("Type a number from 0 to 255: ")
        try:
            num = int(num)
            if 0 <= num <= 255:
                GPIO.output(dac, dec2bin(num))
                voltage = float(num) / 256.0 * 3.3
                print(f"Output voltage is about {voltage:.4} volt")
            else:
                if num < 0:
                    print("Number have to be >=0")
                elif num > 255:
                    print("Number is out of range [0,255]")
        except Exception:
            if num == "q": break
            print("You have to type a number, not string")

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
    print("EOP")
