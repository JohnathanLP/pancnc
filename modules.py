from PIL import Image
import time

#threshold = (0,   15,  31,  47,  63,  80,  95,  111, 127, 191, 255)
#threschar = ('@', '%', '#', '*', '+', '=', '-', '!', ':', '^', '.')

threshold = [0,   31,  62,  93,  125, 156, 187, 218, 255]
threschar = ['@', '%', '#', '+', '=', '-', ':', '^', '.']


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

    threshold[4] = rangeAverage(shades, 0, 255)
    threshold[2] = rangeAverage(shades, 0, threshold[4])
    threshold[6] = rangeAverage(shades, threshold[4], 255)

    threshold[1] = rangeAverage(shades, 0, threshold[2])
    threshold[3] = rangeAverage(shades, threshold[2], threshold[4])
    threshold[5] = rangeAverage(shades, threshold[4], threshold[6])
    threshold[7] = rangeAverage(shades, threshold[6], 255)

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


# print ascii image to terminal one island at a time
def islandPrint():
    # get image name from user, open image
    imName = raw_input("Image name (without extension):") 
    fileIn = open("parsed/instructions/" + imName + ".txt")
    print("Instructions file opened successfully\n\n")
    # print fileIn.read()
    
    wide, high = fileIn.readline().split(',',1)

    wide = int(wide)
    high = int(high)

    print wide
    print high
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
#            print ("coord\n")
            x,y = line.split(',',1)
            x = int(x)
            y = int(y)
            printer[x][y] = threschar[threshold.index(shade)]

        else:
            if int(line) > 0:
#                print ("shade\n")
                shade = int(line)
#            else:
#                print ("EOI\n")

#        print printer

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
    

# partition image into contiguous islands of the same color
def imagePartition():
    # get image name from user, open image
    imName = raw_input("Image name (without extension):") 
    imIn = Image.open("parsed/images/" + imName + ".png")
    pixIn = imIn.load()
    print "Image loaded successfully!"

    # get image size and mode, print for debugging
    wide, high = imIn.size
    print wide, high
    print imIn.mode

    islands = []
    
    # iterate through entire image, add each pixel to its own island   
    i = 0
    j = 0
    while j < high:
        while i < wide:
            islands.append([(i,j)])                    
            i+=1
        i=0
        j+=1

    print("island partitioning is about to begin!")
    print("there are now: " + str(len(islands)) + " islands")

    # iterate through entire image, check neighbors for same color
    # if neighbor is same color, check if same island
    i = 0
    j = 0
    while j < high:
        while i < wide:
            currPix = pixIn[i,j][0]
            # test right
            if i < wide-1:
                if currPix == pixIn[i+1,j][0]:
                    currIsland = searchIslands((i,j,pixIn[i,j][0]), islands)
                    testIsland = searchIslands((i+1,j,pixIn[i+1,j][0]), islands)
                    if currIsland != testIsland:
                        islands[currIsland].extend(islands[testIsland])
                        islands.pop(testIsland)
            # test up
            if j > 0:
                if currPix == pixIn[i,j-1][0]:
                    currIsland = searchIslands((i,j), islands)
                    testIsland = searchIslands((i,j-1), islands)
                    if currIsland != testIsland:
                        islands[currIsland].extend(islands[testIsland])
                        islands.pop(testIsland)
            # test left
            if i > 0:
                if currPix == pixIn[i-1,j][0]:
                    currIsland = searchIslands((i,j), islands)
                    testIsland = searchIslands((i-1,j), islands)
                    if currIsland != testIsland:
                        islands[currIsland].extend(islands[testIsland])
                        islands.pop(testIsland)
            # test down
            if j < high-1:
                if currPix == pixIn[i,j+1][0]:
                    currIsland = searchIslands((i,j), islands)
                    testIsland = searchIslands((i,j+1), islands)
                    if currIsland != testIsland:
                        islands[currIsland].extend(islands[testIsland])
                        islands.pop(testIsland)

            i+=1
        i=0
        j+=1

    print("island partitioning complete!")
    print("there are now: " + str(len(islands)) + " islands")

    for island in islands:
        if pixIn[island[0][0],island[0][1]][1] == 0:
            islands.pop(islands.index(island))

    print("transparency removed!")
    print("there are now: " + str(len(islands)) + " islands")


    # sort islands from darkest to lightest
    sorted = False
    while sorted == False:
        sorted = True
        iter = 0
        while iter < len(islands)-1:
            first  = pixIn[islands[iter][0][0], islands[iter][0][1]]
            second = pixIn[islands[iter+1][0][0], islands[iter+1][0][1]]
            if first > second:
                temp = islands[iter]
                islands[iter] = islands[iter+1]
                islands[iter+1] = temp
                sorted = False
            iter += 1

    # sort pixels within each island left to right, top to bottom
    for island in islands:
        island.sort()

    reportOut = open("parsed/islands/" + imName + ".txt", "w+")
    
    # create file with user-friendly report on each island
    for island in islands:
        reportOut.write("Island: " + str(islands.index(island)) + "\n")
        reportOut.write("size: " + str(len(island)) + "\n")
        reportOut.write("value: " + str(islandValue(island, pixIn)) + "\n")
        reportOut.write(str(island) + "\n\n\n")

    reportOut.close()

    instrOut = open("parsed/instructions/" + imName + ".txt", "w+")
    
    # create file with machine-friendly instructions to print image
    instrOut.write(str(wide) + "," + str(high) + "\n")
    for island in islands:
        instrOut.write(str(pixIn[island[0][0], island[0][1]][0]) + "\n")
        for pixel in island:
            instrOut.write(str(pixel[0]) + "," + str(pixel[1]) + "\n")
        instrOut.write(str(-1) + "\n")    

    instrOut.close()

    imIn.close()


# find which island contains a specific coordinate
def searchIslands(coord, islands):
    for island in islands:
        if island.count(coord) > 0:
            return islands.index(island)

# get value of pixels in an island
def islandValue(island, image):
    return str(image[island[0][0],island[0][1]][0])

# print parsed image to ASCII
def asciiPrint():
    # get image name from user, open image
    imName = raw_input("Image name (without extension):") 
    imIn = Image.open("parsed/images/" + imName + ".png")
    pixIn = imIn.load()
    print "Image loaded successfully!"

    # get image size and mode, print for debugging
    wide, high = imIn.size
    print wide, high
    print imIn.mode

    #parse through image, print to terminal
    i = 0
    j = 0
    line = ""

    while j < high:
        while i < wide:
            val = pixIn[i,j]
            if val[1] != 0:
                for thresh in threshold:
                    if val[0] == thresh:
                        line += threschar[threshold.index(thresh)].ljust(2)
                #line += str(val[0]).ljust(4)
            else:
                line += "  "
            i+=1
        print line
        line = ""
        i=0
        j+=1

    imIn.close()



# load, desaturate, and scale image
def imageParse(): 
    # get image name from user, open image
    imName = raw_input("Image name (without extension):") 
    imIn = Image.open("input/" + imName + ".png")
    pixIn = imIn.load()
    print "Image loaded successfully!"

    # get image size and mode, print for debugging
    wide, high = imIn.size
    print wide, high
    print imIn.mode

    # create output image
    imOut = Image.new("RGBA", (wide,high), "white")
    pixOut = imOut.load()

    # parse through image, replace RGB values with an average
    i = 0
    j = 0
    while j < high:
      while i < wide: 
        pixOut[i,j] = pixIn[i,j]
        ave = pixIn[i,j][0]+pixIn[i,j][1]+pixIn[i,j][2]
        ave /= 3
        pixOut[i,j] = (ave,ave,ave, pixIn[i,j][3])
        i+=1
      i=0
      j+=1

    # scale output image to desired size
    wideOut = 32
    highOut = 32
    imOut = imOut.resize((wideOut,highOut))

    # convert output image to black and white image
    imOut = imOut.convert("LA")

    # parse through output image, round up to nearest threshold
    pixOut = imOut.load()
    i = 0
    j = 0
    while j < highOut:
        while i < wideOut:
            val = pixOut[i,j]
            # if pixel is transparent, set it to white and full transparent
            if val[1] == 0:
                pixOut[i,j] = (255,0)
            # otherwise round and set to full opaque
            else:
                for thresh in threshold:
                    if val[0] < thresh:
                        pixOut[i,j] = (thresh, 255)
                        break
            i+=1
        i=0
        j+=1

    # save output image
    imOut.save("parsed/images/" + imName + ".png")
    # this should work, I'm not sure why it doesn't
    imOut.close()

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


