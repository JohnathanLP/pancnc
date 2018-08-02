
import modules

done = False

print "Welcome\n"

while not done:
    modules.reportImage()
    print "\n"

    print "Select option:\n"
    print "1 Load image"
    print "2 Scale, desaturate, and decontrast loaded image"
    print "3 Print ASCII image"
    print "9 Quit"

    menu = raw_input()

    if menu == "1":
        modules.loadImage()
    elif menu == "2":
        modules.parseImage()
    elif menu == "3":
        modules.previewImage()
    elif menu == "4":
        modules.islandPrint()
    elif menu == "5":
        modules.convertImage()
    elif menu == "6":
        modules.calibrateThresh()
    elif menu == "7":
        modules.loadImage()
    elif menu == "8":
        print "\nunimplemented\n"
    elif menu == "9":
        print "\nExiting\n"
        done = True
    else:
        print "\nInvalid selection\n"

    print "\n\n- - - - - -\n\n"
