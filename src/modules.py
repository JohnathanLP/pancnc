from PIL import Image
from os import system
from panjob import PanJob
#TODO this is bad and I should feel bad v
from config import *
import time

current_job = PanJob()

# Variables to store information about the currently loaded (raw) image file
imgName  = ""
rawImg   = None
rawPix   = None
rawWide  = None
rawHigh  = None

parsImg  = None
parsPix  = None

# loads an image
def loadImage():
    global current_job

    current_job.filename = input("Image name (without extension, place file in input directory): ") 

    try:
        current_job.raw_image = Image.open("input/" + current_job.filename + ".png")
    except:
        print("file failed to open")
        imgName = ""
        return

    current_job.raw_pixels = current_job.raw_image.load()
    print("Image loaded successfully!")
    print("Dimensions: " + str(current_job.rawWide()) + ", " + str(current_job.rawHigh()))
    print("Image Mode: " + current_job.rawMode())

# load, desaturate, and scale image
# takes in raw image, saves edited .png file and loads pixels into parsPix array
def parseImage():
    global current_job

    if current_job.raw_image == None:
        print("No image loaded")
        return

    # create parsed image from raw image, resize image, desaturate
    current_job.parsed_image = current_job.raw_image.resize((parsWide, parsHigh)).convert("LA")

    # parse through image, remove any partial transparency
    current_job.parsed_pixels = current_job.parsed_image.load()
    for j in range(0,parsHigh):
        for i in range(0,parsWide):
            if current_job.parsed_pixels[i,j][1] != 255:
                current_job.parsed_pixels[i,j] = (0,0)
            else:
                current_job.parsed_pixels[i,j] = (current_job.parsed_pixels[i,j][0], 255)

    # TODO Mirror image

    # save output image
    current_job.parsed_image.save("parsed/images/" + current_job.filename + ".png")

    print("Image parsed successfully!")
    print("Parsed image saved to \'parsed/images" + current_job.filename + ".png\'")

# print parsed image to ASCII
# prints from parsPix array
def previewImage():
    global current_job
    # parse through image, print to terminal
    for j in range(0,parsHigh):
        for i in range(0,parsWide):
            pixel = current_job.parsed_pixels[i,j]
#            print(threschar[int(pixel[0]/threshold_size)] if pixel[1]>0 else ' ',end=' ')
#            print(int(pixel[0]/threshold_size) if pixel[1]>0 else ' ',end=' ')
            threshold_index = 255/6
            threshold_index = int(pixel[0]/threshold_index)
            if pixel[1]>0:
                print("\033[;" + str(40+threshold_index) + "m" + str(threshold_index),end=' ')
            else:
                print('\033[0m ',end=' ')
        print('\033[0m')


# partition image into contiguous islands of the same color
# loads from parsPix array, outputs .pcode file
def partitionImage():
    global current_job

    islands = []

    for j in range(parsHigh):
        for i in range(parsWide):
            if current_job.parsed_pixels[i,j][1] > 0:
                islands.append([(i,j)])

    print("island partitioning is about to begin!")
    print("there are initially: " + str(len(islands)) + " islands")

    for j in range(parsHigh):
        for i in range(parsWide):
            current_pixel = current_job.parsed_pixels[i,j]
            
            #test right
#            if i<parsWide-1:
#                if iint(current_pixel[0]/threshold_size) == int(current_job.parsed_pixels[i+1,j][0]):
                                        

def partitionImageOld():
    global parsImg
    global parsPix
    global parsWide
    global parsHigh
    global rangeSize

    islands = []
    
    # iterate through entire image, add each pixel to its own island   
    for j in range(0, parsHigh):
        for i in range(0,parsWide):
            islands.append([(i,j)])                    

    print("island partitioning is about to begin!")
    print("there are now: " + str(len(islands)) + " islands")

    # iterate through entire image, check neighbors for same color (within same range)
    # if neighbor is same color, check if same island
    for j in range(0, parsHigh):
        for i in range(0,parsWide):
            currPix = parsPix[i,j][0]
            # test right
            if i < parsWide-1:
                if int(currPix/rangeSize) == int(parsPix[i+1,j][0]/rangeSize):
#                if roundToThresh(currPix) == roundToThresh(parsPix[i+1,j][0]):
                    currIsland = searchIslands((i,j), islands)
                    testIsland = searchIslands((i+1,j), islands)
                    if currIsland != testIsland:
                        islands[currIsland].extend(islands[testIsland])
                        islands.pop(testIsland)
            # test up
            if j > 0:
                if int(currPix/rangeSize) == int(parsPix[i,j-1][0]/rangeSize):
#                if roundToThresh(currPix) == roundToThresh(parsPix[i,j-1][0]):
                    currIsland = searchIslands((i,j), islands)
                    testIsland = searchIslands((i,j-1), islands)
                    if currIsland != testIsland:
                        islands[currIsland].extend(islands[testIsland])
                        islands.pop(testIsland)
            # test left
            if i > 0:
                if int(currPix/rangeSize) == int(parsPix[i-1,j][0]/rangeSize):
#                if roundToThresh(currPix) == roundToThresh(parsPix[i-1,j][0]):
                    currIsland = searchIslands((i,j), islands)
                    testIsland = searchIslands((i-1,j), islands)
                    if currIsland != testIsland:
                        islands[currIsland].extend(islands[testIsland])
                        islands.pop(testIsland)
            # test down
            if j < parsHigh-1:
                if int(currPix/rangeSize) == int(parsPix[i,j+1][0]/rangeSize):
#                if roundToThresh(currPix) == roundToThresh(parsPix[i,j+1][0]):
                    currIsland = searchIslands((i,j), islands)
                    testIsland = searchIslands((i,j+1), islands)
                    if currIsland != testIsland:
                        islands[currIsland].extend(islands[testIsland])
                        islands.pop(testIsland)

            # test up, right
            if j > 0 and i < parsWide-1:
                if int(currPix/rangeSize) == int(parsPix[i+1,j-1][0]/rangeSize):
#                if currPix == parsPix[i+1,j-1][0]:
                    currIsland = searchIslands((i,j), islands)
                    testIsland = searchIslands((i+1,j-1), islands)
                    if currIsland != testIsland:
                        islands[currIsland].extend(islands[testIsland])
                        islands.pop(testIsland)
            
            # test up, left
            if j > 0 and i > 0:
                if int(currPix/rangeSize) == int(parsPix[i-1,j-1][0]/rangeSize):
#                if currPix == parsPix[i-1,j-1][0]:
                    currIsland = searchIslands((i,j), islands)
                    testIsland = searchIslands((i-1,j-1), islands)
                    if currIsland != testIsland:
                        islands[currIsland].extend(islands[testIsland])
                        islands.pop(testIsland)
            
            # test down, left
            if j < parsHigh-1 and i > 0:
                if int(currPix/rangeSize) == int(parsPix[i-1,j+1][0]/rangeSize):
#                if currPix == parsPix[i-1,j+1][0]:
                    currIsland = searchIslands((i,j), islands)
                    testIsland = searchIslands((i-1,j+1), islands)
                    if currIsland != testIsland:
                        islands[currIsland].extend(islands[testIsland])
                        islands.pop(testIsland)
            
            # test down, right
            if j < parsHigh-1 and i < parsWide-1:
                if int(currPix/rangeSize) == int(parsPix[i+1,j+1][0]/rangeSize):
#                if currPix == parsPix[i+1,j+1][0]:
                    currIsland = searchIslands((i,j), islands)
                    testIsland = searchIslands((i+1,j+1), islands)
                    if currIsland != testIsland:
                        islands[currIsland].extend(islands[testIsland])
                        islands.pop(testIsland)


    print("island partitioning complete!")
    print("there are now: " + str(len(islands)) + " islands")

    for island in islands:
        if parsPix[island[0][0],island[0][1]][1] != 255:
            islands.pop(islands.index(island))

    print("transparency removed!")
    print("there are now: " + str(len(islands)) + " islands")

    # sort pixels within each island left to right, top to bottom
    for island in islands:
        island.sort()

    # sort islands by start point from left to right, top to bottom
    sorted = False
    while sorted == False:
        sorted = True
        iter = 0
        while iter < len(islands)-1:
            first = islands[iter][0][0]
            second = islands[iter+1][0][0]
            if first > second:
                temp = islands[iter]
                islands[iter] = islands[iter+1]
                islands[iter+1] = temp
                sorted = False
            iter += 1

    sorted = False
    while sorted == False:
        sorted = True
        iter = 0
        while iter < len(islands)-1:
            first = islands[iter][0][1]
            second = islands[iter+1][0][1]
            if first > second:
                temp = islands[iter]
                islands[iter] = islands[iter+1]
                islands[iter+1] = temp
                sorted = False
            iter += 1

    # sort islands from darkest to lightest
    sorted = False
    while sorted == False:
        sorted = True
        iter = 0
        while iter < len(islands)-1:
            first  = (parsPix[islands[iter][0][0], islands[iter][0][1]][0])/rangeSize
            second = (parsPix[islands[iter+1][0][0], islands[iter+1][0][1]][0])/rangeSize
            if first > second:
                temp = islands[iter]
                islands[iter] = islands[iter+1]
                islands[iter+1] = temp
                sorted = False
            iter += 1

    # TODO remove this, depreciated
    # create file with user-friendly report on each island
    reportOut = open("parsed/islands/" + imgName + ".txt", "w+")
    
    for island in islands:
        reportOut.write("Island: " + str(islands.index(island)) + "\n")
        reportOut.write("size: " + str(len(island)) + "\n")
        reportOut.write("value: " + str(islandValue(island, parsPix)) + "\n")
        reportOut.write(str(island) + "\n\n\n")

    reportOut.close()

    # TODO remove this, depreciated
    # create file with simulator-friendly instructions to print image
    instrOut = open("parsed/simulator/" + imgName + ".txt", "w+")
    
    instrOut.write(str(parsWide) + "," + str(parsHigh) + "\n")
    for island in islands:
        instrOut.write(str(parsPix[island[0][0], island[0][1]][0]) + "\n")
        for pixel in island:
            instrOut.write(str(pixel[0]) + "," + str(pixel[1]) + "\n")
        instrOut.write(str(-1) + "\n")    
    
    instrOut.close()

    # create file with machine-friendly instructions to print pancake
    codeOut = open("parsed/pcode/" + imgName + ".pcode", "w+")

    # first line reserved for version, etc.
    codeOut.write("pancode version 1.0\n")
    
    # second line reserved for dimensions (in pixels)
    codeOut.write(str(parsWide) + "," + str(parsHigh) + "\n")
    
    codeOut.write("start\n")

    lastShade = 255

    # iterate through each island
    for island in islands:
        # iterate through each pixel
        for pixel in island:
            # move to pixel
            # TODO make this configurable
            mmperpixel = 1
            codeOut.write("M " + str(pixel[0] * mmperpixel) + " " + str(pixel[1] * mmperpixel) + "\n")
            # extrude then retract some to prevent drips
            # TODO make this configurable
            codeOut.write("E 1 1\n")
            codeOut.write("E -1 .5\n")

        # delay before moving to next island
        # TODO Fix this - should pause between shades, not islands
        # May require rewrite of partitioning, which honestly should
        # be done anyway, it looks like it was written by an entire
        # troop of monkeys.
        if (parsPix[island[0][0], island[0][1]][0])/rangeSize != lastShade:
            codeOut.write("D 10\n")
        lastShade = (parsPix[island[0][0], island[0][1]][0])/rangeSize

    codeOut.write("end\n")
    codeOut.close()

# rounds off shades into a given number of steps
def threshImage():
    global numThresh

    # find the range of each threshhold
    ranThresh = int(255/numThresh)
    print("Range of threshholds" + str(ranThresh))

# print ascii image to terminal one island at a time
def printImage():
    global imgName
    global delay
   
    # TODO test for file open failure
    fileIn = open("parsed/pcode/" + imgName + ".pcode")
    print("Instructions file opened successfully\n\n")
    
    # ignore first line
    # TODO Version checking for GCode version
    fileIn.readline()

    wide, high = fileIn.readline().split(',',1)
    print("Dimensions: "+ wide + ", " + high)
    
    wide = int(wide)
    high = int(high)

    shade = -1

    # create blank simulated print surface
    printer = []
    for i in range(0,high):
        temp = []
        for j in range(0,wide):
            temp.append(" ")
        printer.append(temp)

    # represents the location of the extruder
    posX = 0
    posY = 0

    for line in fileIn:
        # split line into args
        args = line.split()

        # start command
        if args[0] == "start":
            print("Beginning print")

        # end command
        elif args[0] == "end":
            # TODO terminate print
            print("Print complete!")

        # move command
        elif args[0] == "M":
            posX = int(args[1])
            posY = int(args[2])

        # manual extrude command
        elif args[0] == "E":
            printer[posX][posY] = 0
            
        # continuous extrude command

        # delay command
        elif args[0] == "D":
            for j in range(0,high):
                for i in range(0,wide):
                    if printer[i][j] != " ":
                        printer[i][j] += 1

        # tone command

        # display progress
        output = "\n\n\n\n-----\n\n\n\n"
        for j in range(0,high):
            temp = ""
            for i in range(0,wide):
                #temp += str(printer[i][j]).ljust(2)
                if printer[i][j] != " ":
                    temp += threschar[printer[i][j]].ljust(2)
                else:
                    temp += "  "

            output += (temp + "\n")
        
        print(output)
        time.sleep(delay)
        system('clear')
    
    fileIn.close()


#--------------------#

def cleanup():
    current_job.cleanup()

#--------------------#

def roundToThresh(val_in):
    return int(val_in/32)

# find which island contains a specific coordinate
def searchIslands(coord, islands):
    for island in islands:
        if island.count(coord) > 0:
            return islands.index(island)

# get value of pixels in an island
def islandValue(island, image):
    return str(image[island[0][0],island[0][1]][0])

