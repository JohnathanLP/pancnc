import time
import RPi.GPIO as GPIO
#import RPi.GPIO.HIGH as HIGH
#import RPi.GPIO.LOW as LOW

imgName = ""
pCode = None

#TODO Correctly set these pin numbers
xA = [0,1,2,3]
yA = [0,1,2,3]
eA = [0,1,2,3]

step1 = [GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.HIGH]
step2 = [GPIO.HIGH,GPIO.LOW,GPIO.HIGH,GPIO.LOW]
step3 = [GPIO.LOW,GPIO.HIGH,GPIO.HIGH,GPIO.LOW]
step4 = [GPIO.LOW,GPIO.HIGH,GPIO.LOW,GPIO.HIGH]

def initGPIO():
    print "Initializing GPIO..."
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in xA:
        GPIO.setup(pin, GPIO.OUT)
    for pin in yA:
        GPIO.setup(pin, GPIO.OUT)
    for pin in eA:
        GPIO.setup(pin, GPIO.OUT)

def stopGPIO():
    print "Cleaning up GPIO..."
    GPIO.cleanup()

def loadFile():
    global imgName

    imgName = raw_input("Image name (without extension):")
    try:
        pCode = open("parsed/pcode/" + imgName + ".pcode")
    except:
        print "file failed to open"
        imgName = ""
        return
    print "File loaded successfully!"

def printPancake():
    print "Lets do this"

