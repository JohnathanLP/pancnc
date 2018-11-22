import modules
#import motors
import gui
import sys

if len(sys.argv) > 1:
    if sys.argv[1] == "-nogui":
        done = False

        print "Welcome\n"

        while not done:
            modules.reportImage()
            print "\n"

            print "Select option:\n"
            print "1 Load image"
            print "2 Scale and desaturate image"
            print "3 Print ASCII image"
            print "4 Partition image into islands"
            print "5 Simulate printing image"
            print "6 Threshold Image"
            print "7 Run Printer"
            print "8 Fully process image"
            print "9 Quit"

            menu = raw_input()

            if menu == "1":
                modules.loadImage()
            elif menu == "2":
                modules.parseImage()
            elif menu == "3":
                modules.previewImage()
            elif menu == "4":
                modules.partitionImage()
            elif menu == "5":
                modules.printImage()
            elif menu == "6":
                modules.threshImage()
            #TODO move this to thread
            elif menu == "7":
                choice = raw_input("Are you sure? (y/n)")
                if choice == 'y':
                    motors.initGPIO()
                    motors.loadFile()
                    motors.printPancake()
                    motors.stopGPIO()
            elif menu == "8":
                modules.loadImage()
                modules.parseImage()
                modules.previewImage()
                modules.partitionImage()
            elif menu == "9":
                print "\nExiting\n"
                modules.closeImages()
                done = True
            else:
                print "\nInvalid selection\n"

            print "\n\n- - - - - -\n\n"
else: 
    gui.launch()
