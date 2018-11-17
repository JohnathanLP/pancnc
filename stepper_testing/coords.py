import RPi.GPIO as GPIO
import time
import math

x_pos = 0
y_pos = 0

x_lim = 100000
y_lim = 100000

s_p_m = 50
s_p_j = 50

x_stp = 5
x_dir = 6

x_ms1 = 26
x_ms2 = 19
x_ms3 = 13

y_stp = 21
y_dir = 20

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(x_stp, GPIO.OUT)
GPIO.setup(x_dir, GPIO.OUT)
GPIO.setup(x_ms1, GPIO.OUT)
GPIO.setup(x_ms2, GPIO.OUT)
GPIO.setup(x_ms3, GPIO.OUT)

GPIO.setup(y_stp, GPIO.OUT)
GPIO.setup(y_dir, GPIO.OUT)

control = ''

def gotoXY(x_in, y_in):
    global x_pos
    global y_pos
    global s_p_m
    
    x_tra = (x_in - x_pos)
    y_tra = (y_in - y_pos)

    print("testing " + str(x_tra) + "," + str(y_tra))

    if(x_tra > 0):
        GPIO.output(x_dir, GPIO.HIGH)
    else:
        GPIO.output(x_dir, GPIO.LOW)
        x_tra = -x_tra

    if(y_tra > 0):
        GPIO.output(y_dir, GPIO.HIGH)
    else:
        GPIO.output(y_dir, GPIO.LOW)
        y_tra = -y_tra

    count = 0
    while count < x_tra:
        GPIO.output(x_stp, GPIO.HIGH)
        # sleep for 500 uS
        time.sleep(0.001)
        GPIO.output(x_stp, GPIO.LOW)
        # sleep for 550 uS
        time.sleep(0.001)
        count += 1

    count = 0
    while count < y_tra:
        GPIO.output(y_stp, GPIO.HIGH)
        # sleep for 500 uS
        time.sleep(0.001)
        GPIO.output(y_stp, GPIO.LOW)
        # sleep for 550 uS
        time.sleep(0.001)
        count += 1

    x_pos = x_in
    y_pos = y_in

def drawCircle(rad):
    global x_pos
    global y_pos

    x_ori = x_pos
    y_ori = y_pos
    
    deg = 0
    while deg < 360:
        gotoXY(x_ori + math.floor(math.cos(math.radians(deg))*rad), y_ori + math.floor(math.sin(math.radians(deg))*rad))
        deg += 2

    gotoXY(x_ori, y_ori)

try:
    GPIO.output(x_dir, GPIO.LOW)
    GPIO.output(y_dir, GPIO.LOW)
    GPIO.output(x_ms1, GPIO.LOW)
    GPIO.output(x_ms2, GPIO.LOW)
    GPIO.output(x_ms3, GPIO.LOW)

    while True:
        count = 0
        control = raw_input("")

        if (control == "a" or control == "d"):# and x_pos >= 0 and x_pos <= x_lim:
            if control == "a":
                GPIO.output(x_dir, GPIO.LOW)
                x_pos -= s_p_j#s_p_m * s_p_j
            elif control == "d":
                GPIO.output(x_dir, GPIO.HIGH)
                x_pos += s_p_j#s_p_m * s_p_j
            while count < s_p_m:
                GPIO.output(x_stp, GPIO.HIGH)
                # sleep for 500 uS
                time.sleep(0.001)
                GPIO.output(x_stp, GPIO.LOW)
                # sleep for 550 uS
                time.sleep(0.001)
                count += 1

        elif (control == "w" or control == "s"):# and y_pos >= 0 and y_pos <= y_lim:
            if control == "w":
                GPIO.output(y_dir, GPIO.LOW)
                y_pos -= s_p_j#s_p_m * s_p_j
            elif control == "s":
                GPIO.output(y_dir, GPIO.HIGH)
                y_pos += s_p_j#s_p_m * s_p_j
            while count < s_p_m:
                GPIO.output(y_stp, GPIO.HIGH)
                # sleep for 500 uS
                time.sleep(0.001)
                GPIO.output(y_stp, GPIO.LOW)
                # sleep for 550 uS
                time.sleep(0.001)
                count += 1

        if control == "r":
            x_pos = 0
            y_pos = 0

        if control == "g":
            x_tar = input("X coord: ")
            y_tar = input("Y coord: ")
            gotoXY(x_tar, y_tar)

        if control == "h":
            gotoXY(0, 0)

        if control == "c":
            rad = input("Radius: ")
            drawCircle(rad)

        print ("coords: " + str(x_pos) + "," + str(y_pos))
except KeyboardInterrupt:
    GPIO.cleanup()

