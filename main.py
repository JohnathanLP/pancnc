
import modules

print "Welcome\n"
print "Select option:\n"
print "1 Load, desaturate and scale image"
print "2 Print an image to ASCII art in terminal"
print "3 "

menu = raw_input()
print menu

if menu == "1":
    modules.imageParse()
elif menu == "2":
    modules.asciiPrint()
elif menu == "3":
    print "unimplemented"

