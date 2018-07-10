from PIL import Image

threshold = (0,   15,  31,  47,  63,  80,  95,  111, 127, 191, 255)
threschar = ('@', '%', '#', '*', '+', '=', '-', '!', ':', '^', '.')

# print ascii image to terminal one island at a time
def islandPrint():
    # get image name from user, open image
    imName = raw_input("Image name (without extension):") 
    imIn = Image.open("parsed/images/" + imName + ".png")
    pixIn = imIn.load()
    print "Image loaded successfully!"

    # get image size and mode, print for debugging
    wide, high = imIn.size
    print wide, high
    print imIn.mode

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

    #for island in islands:
    #    print(island)
    #    for pix in island:
    #        print(pixIn[pix[0], pix[1]])
    
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
                    currIsland = searchIslands((i,j), islands)
                    testIsland = searchIslands((i+1,j), islands)
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

    fileOut = open("parsed/islands/" + imName + ".txt", "w+")

    for island in islands:
        island.sort()

    for island in islands:
        fileOut.write("Island: " + str(islands.index(island)) + "\n")
        fileOut.write("size: " + str(len(island)) + "\n")
        #fileOut.write("value: " + str(pixIn[island[0][0],island[0][1]][0]) + "\n")
        fileOut.write("value: " + str(islandValue(island, pixIn)) + "\n")
        fileOut.write(str(island) + "\n\n\n")

    fileOut.close()

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
    imIn = Image.open(imName + ".png")
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
    ##threshold = (0,31,63,95,127,159,191,223,255)
    #threshold = (0,15,31,47,63,80,95,111,127,191,255)
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

