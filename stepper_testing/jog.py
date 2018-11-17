import RPi.GPIO as GPIO
import time

x_stp = 5
x_dir = 6

x_ms1 = 26
x_ms2 = 19
x_ms3 = 13

x_d = 0

y_stp = 21
y_dir = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(x_stp, GPIO.OUT)
GPIO.setup(x_dir, GPIO.OUT)
GPIO.setup(x_ms1, GPIO.OUT)
GPIO.setup(x_ms2, GPIO.OUT)
GPIO.setup(x_ms3, GPIO.OUT)

GPIO.setup(y_stp, GPIO.OUT)
GPIO.setup(y_dir, GPIO.OUT)

control = ''

try:
    GPIO.output(x_dir, GPIO.LOW)
    GPIO.output(y_dir, GPIO.LOW)
    GPIO.output(x_ms1, GPIO.LOW)
    GPIO.output(x_ms2, GPIO.LOW)
    GPIO.output(x_ms3, GPIO.LOW)

    while True:
        count = 0
        control = raw_input("")
        if control == "a":
            GPIO.output(x_dir, GPIO.LOW)
        elif control == "d":
            GPIO.output(x_dir, GPIO.HIGH)
        elif control == "w":
            GPIO.output(y_dir, GPIO.LOW)
        elif control == "s":
            GPIO.output(y_dir, GPIO.HIGH)

        if control == "a" or control == "d":
            while count < 50:
                GPIO.output(x_stp, GPIO.HIGH)
                # sleep for 500 uS
                time.sleep(0.001)
                GPIO.output(x_stp, GPIO.LOW)
                # sleep for 550 uS
                time.sleep(0.001)
                count += 1
        elif control == "w" or control == "s":
            while count < 50:
                GPIO.output(y_stp, GPIO.HIGH)
                # sleep for 500 uS
                time.sleep(0.001)
                GPIO.output(y_stp, GPIO.LOW)
                # sleep for 550 uS
                time.sleep(0.001)
                count += 1

except KeyboardInterrupt:
    GPIO.cleanup()

