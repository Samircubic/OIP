import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(8, GPIO.OUT)

n=10
p = GPIO.PWM(8, 1000)
p.start(0)

try:
    while True:
        f = int(input())
        p.ChangeDutyCycle(f)
        print(3.3*f/100)

finally:
    p.stop()
    GPIO.output(8,0)
    GPIO.cleanup()
