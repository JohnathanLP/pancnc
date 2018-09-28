
import modules

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
    elif menu == "7":
        print "\nunimplemented\n"
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
