
import modules

done = False

while not done:
    print "Welcome\n"
    print "Select option:\n"
    print "1 Load, desaturate and scale image"
    print "2 Print an image to ASCII art in terminal"
    print "3 Quit"

    menu = raw_input()

    if menu == "1":
        modules.imageParse()
    elif menu == "2":
        modules.asciiPrint()
    elif menu == "3":
        #print "unimplemented"
        done = True
    elif menu == "4":
        print "unimplemented"
    elif menu == "5":
        print "unimplemented"
    elif menu == "6":
        print "unimplemented"
    elif menu == "7":
        print "unimplemented"
    elif menu == "8":
        print "unimplemented"
    elif menu == "9":
        print "unimplemented"
