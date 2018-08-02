from PIL import Image
import time

#threshold = (0,   15,  31,  47,  63,  80,  95,  111, 127, 191, 255)
#threschar = ('@', '%', '#', '*', '+', '=', '-', '!', ':', '^', '.')

#threshold = [0,   31,  62,  93,  125, 156, 187, 218, 255]
#threschar = ['@', '%', '#', '+', '=', '-', ':', '^', '.']

threshold = [0,   62,  125, 187, 255]
threschar = ['@', '#', '=', ':', '.']

imgName  = ""
rawImg   = None
rawPix   = None
rawWide  = None
rawHigh  = None

parsImg  = None
parsPix  = None
# TODO Allow for different sizes/resolutions
parsHigh = 32
parsWide = 32

# loads an image
def loadImage():
    global imgName
    global rawImg
    global rawPix
    global rawWide
    global rawHigh

    imgName = raw_input("Image name (without extension):") 
    rawImg = Image.open("input/" + imgName + ".png")
    rawPix = rawImg.load()
    # TODO check for load failure, image not existing
    print "Image loaded successfully!"

    # report image size and mode
    rawWide, rawHigh = rawImg.size
    print "Dimensions: " + str(rawWide) + ", " + str(rawHigh)
    print "Image Mode: " + rawImg.mode

# reports currently loaded image
def reportImage():
    global imgName

    if imgName == "":
        print "No image loaded"
    else:
        print "Image loaded: " + imgName + ".png"

# load, desaturate, and scale image
def parseImage(): 
    global imgName
    global rawImg
    global rawPix
    global rawWide
    global rawHigh

    global parsImg
    global parsPix
    global parsWide
    global parsHigh

    # create parsed image from raw image, resize image, desaturate
    parsImg = rawImg
    parsImg = parsImg.resize((parsWide, parsHigh))
    parsImg = parsImg.convert("LA")

    # parse through image, remove any partial transparency
    parsPix = parsImg.load()
    for j in range(0,parsHigh):
        for i in range(0,parsWide):
            if parsPix[i,j][1] == 0:
                parsPix[i,j] = (255,0)
            else:
                parsPix[i,j] = (parsPix[i,j][0], 255)

    # save output image
    parsImg.save("parsed/images/" + imgName + ".png")

# print parsed image to ASCII
def previewImage():
    global parsPix
    global parsHigh
    global parsWide

    #parse through image, print to terminal
    line = ""
    
    for j in range(0,parsHigh):
        for i in range(0,parsWide):
            val = parsPix[i,j]
            if val[1] != 0:
                line += threschar[threshold.index(roundToThresh(val[0]))].ljust(2)
            else:
                line += "  "
            i+=1
        print line
        line = ""
        i=0
        j+=1


# partition image into contiguous islands of the same color
def partitionImage():
    global parsImg
    global parsPix
    global parsWide
    global parsHigh

    islands = []
    
    # iterate through entire image, add each pixel to its own island   
    for j in range(0, parsHigh):
        for i in range(0,parsWide):
            islands.append([(i,j)])                    

    print("island partitioning is about to begin!")
    print("there are now: " + str(len(islands)) + " islands")

    # iterate through entire image, check neighbors for same color
    # if neighbor is same color, check if same island
    for j in range(0, parsHigh):
        for i in range(0,parsWide):
            currPix = parsPix[i,j][0]
            # test right
            if i < parsWide-1:
                if currPix == parsPix[i+1,j][0]:
                    currIsland = searchIslands((i,j), islands)
                    testIsland = searchIslands((i+1,j), islands)
                    if currIsland != testIsland:
                        islands[currIsland].extend(islands[testIsland])
                        islands.pop(testIsland)
            # test up
            if j > 0:
                if currPix == parsPix[i,j-1][0]:
                    currIsland = searchIslands((i,j), islands)
                    testIsland = searchIslands((i,j-1), islands)
                    if currIsland != testIsland:
                        islands[currIsland].extend(islands[testIsland])
                        islands.pop(testIsland)
            # test left
            if i > 0:
                if currPix == parsPix[i-1,j][0]:
                    currIsland = searchIslands((i,j), islands)
                    testIsland = searchIslands((i-1,j), islands)
                    if currIsland != testIsland:
                        islands[currIsland].extend(islands[testIsland])
                        islands.pop(testIsland)
            # test down
            if j < parsHigh-1:
                if currPix == parsPix[i,j+1][0]:
                    currIsland = searchIslands((i,j), islands)
                    testIsland = searchIslands((i,j+1), islands)
                    if currIsland != testIsland:
                        islands[currIsland].extend(islands[testIsland])
                        islands.pop(testIsland)

    print("island partitioning complete!")
    print("there are now: " + str(len(islands)) + " islands")

    for island in islands:
        if parsPix[island[0][0],island[0][1]][1] == 0:
            islands.pop(islands.index(island))

    print("transparency removed!")
    print("there are now: " + str(len(islands)) + " islands")


    # sort islands from darkest to lightest
    sorted = False
    while sorted == False:
        sorted = True
        iter = 0
        while iter < len(islands)-1:
            first  = parsPix[islands[iter][0][0], islands[iter][0][1]]
            second = parsPix[islands[iter+1][0][0], islands[iter+1][0][1]]
            if first > second:
                temp = islands[iter]
                islands[iter] = islands[iter+1]
                islands[iter+1] = temp
                sorted = False
            iter += 1

    # sort pixels within each island left to right, top to bottom
    for island in islands:
        island.sort()

    reportOut = open("parsed/islands/" + imgName + ".txt", "w+")
    
    # create file with user-friendly report on each island
    for island in islands:
        reportOut.write("Island: " + str(islands.index(island)) + "\n")
        reportOut.write("size: " + str(len(island)) + "\n")
        reportOut.write("value: " + str(islandValue(island, parsPix)) + "\n")
        reportOut.write(str(island) + "\n\n\n")

    reportOut.close()

    instrOut = open("parsed/instructions/" + imgName + ".txt", "w+")
    
    # create file with machine-friendly instructions to print image
    instrOut.write(str(parsWide) + "," + str(parsHigh) + "\n")
    for island in islands:
        instrOut.write(str(parsPix[island[0][0], island[0][1]][0]) + "\n")
        for pixel in island:
            instrOut.write(str(pixel[0]) + "," + str(pixel[1]) + "\n")
        instrOut.write(str(-1) + "\n")    

    instrOut.close()


# print ascii image to terminal one island at a time
def printImage():
    global imgName
   
    # TODO test for file open failure
    fileIn = open("parsed/instructions/" + imgName + ".txt")
    print("Instructions file opened successfully\n\n")
    
    wide, high = fileIn.readline().split(',',1)
    print "Dimensions: "+ wide + ", " + high
    
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


    print("beginning print")

    for line in fileIn:
        # coords
        if "," in line:
            x,y = line.split(',',1)
            x = int(x)
            y = int(y)
            printer[x][y] = threschar[threshold.index(shade)]

        else:
            if int(line) >= 0:
                shade = int(line)
                shade = roundToThresh(shade)

        # display progress
        output = "\n\n\n\n-----\n\n\n\n"
        for j in range(0,high):
            temp = ""
            for i in range(0,wide):
                temp += printer[i][j]
                temp += " "
            output += (temp + "\n")
        
        print output
        time.sleep(.05)
    
    fileIn.close()


#--------------------#

def closeImages():
    if rawImg != None:
        rawImg.close()
    if parsImg != None:
        parsImg.close()

#--------------------#

def roundToThresh(valIn):
    for thresh in threshold:
        if valIn <= thresh:
            return thresh

# find which island contains a specific coordinate
def searchIslands(coord, islands):
    for island in islands:
        if island.count(coord) > 0:
            return islands.index(island)

# get value of pixels in an island
def islandValue(island, image):
    return str(image[island[0][0],island[0][1]][0])

#--------------------#

# calibrate threshold values to get the best resolution
def calibrateThresh():
    # get image name from user, open image
    imName = raw_input("Image name (without extension):") 
    imIn = Image.open("input/" + imName + ".png")
    pixIn = imIn.load()
    print "Image loaded successfully!"

    # get image size and mode, print for debugging
    wide, high = imIn.size
    print wide, high
    print imIn.mode

    shades = []
    for j in range(0,high):
        for i in range(0,wide):
            ave =  pixIn[i,j][0] + pixIn[i,j][1] + pixIn[i,j][2]
#            if pixIn[i,j][3] > 0:
            shades.append(int(ave/3))

#    threshold[4] = rangeAverage(shades, 0, 255)
#    threshold[2] = rangeAverage(shades, 0, threshold[4])
#    threshold[6] = rangeAverage(shades, threshold[4], 255)
#    threshold[1] = rangeAverage(shades, 0, threshold[2])
#    threshold[3] = rangeAverage(shades, threshold[2], threshold[4])
#    threshold[5] = rangeAverage(shades, threshold[4], threshold[6])
#    threshold[7] = rangeAverage(shades, threshold[6], 255)

    threshold[2] = rangeAverage(shades, 0, 255)
    threshold[1] = rangeAverage(shades, 0, threshold[2])
    threshold[3] = rangeAverage(shades, threshold[2], 255)

    imIn.close()


# given an array of numbers and a range, find the average, considering only
# numbers within the range
def rangeAverage(numbers, rangeMin, rangeMax):
    rSum = 0
    count = 0
    for number in numbers:
        if number >= rangeMin and number <=rangeMax:
            rSum += number
            count += 1
    return int(rSum/count)







# convert png image to RGBA png file
def convertImage():
    # get image name from user, open image
    imName = raw_input("Image name (without extension):") 
    imIn = Image.open(imName + ".png")
    print "Image loaded successfully!"

    # get image size and mode, print for debugging
    wide, high = imIn.size
    print wide, high
    print imIn.mode

    # convert image
    imIn.convert("RGBA").save(imName + "_converted.png")

    imIn.close()
