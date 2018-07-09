
import modules

done = False

print "Welcome\n"

while not done:
    print "Select option:\n"
    print "1 Load, desaturate and scale image"
    print "2 Print an image to ASCII art in terminal"
    print "3 Partition an image into contiguous islands"
    print "4 Quit"

    menu = raw_input()

    if menu == "1":
        modules.imageParse()
    elif menu == "2":
        modules.asciiPrint()
    elif menu == "3":
        modules.imagePartition()
    elif menu == "4":
        print "\nExiting..."
        done = True
    elif menu == "5":
        print "\nunimplemented\n"
    elif menu == "6":
        print "\nunimplemented\n"
    elif menu == "7":
        print "\nunimplemented\n"
    elif menu == "8":
        print "\nunimplemented\n"
    elif menu == "9":
        print "\nunimplemented\n"
    else:
        print "\nInvalid selection\n"

    print "\n\n- - - - - -\n\n"
