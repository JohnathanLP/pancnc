from PIL import Image

threshold = (0,   15,  31,  47,  63,  80,  95,  111, 127, 191, 255)
threschar = ('@', '%', '#', '*', '+', '=', '-', '!', ':', '^', '.')

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

    # array of boolean representing which pixels have already been hit
    pixTchd = [[False] * wide for x in range(high)]

    # number of islands
    islandCnt = 0

    # pixel queue
    queue = []

    # parse through image, partition and print to terminal
    i = 0
    j = 0
    while j < high:
        while i < wide:
            # if pixel has not been touched, touch it, create a new 
            # island and add that pixel. add all neighbors of that pixel 
            # to queue. parse through queue, if a pixel has not been 
            # touched, and is the same value as the first pixel, touch 
            # it, add it to the island, add all neighbors to queue. 
            # remove current pixel from queue.
        
            if pixTchd[i][j] == False:
                pixTchd[i][j] = True
                queue.append((i,j))
                x = i
                y = j
                while len(queue)>0:
                    print "remaining in queue: " + str(len(queue))
                    # test up
                    if j>0:
                        if pixTchd[x][y-1] == False and pixIn[x,y] == pixIn[x,y-1]:
                            queue.append((x,y-1))
                            pixTchd[x][y-1] = True
                    # test right
#                    if i<wide-1:

                    # test down
#                    if j<high-1:

                    # test left
#                    if i>0:


                    queue.pop()

            islandCnt += 1

            i+=1
        i=0
        j+=1



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

    #threshold = (0,   15,  31,  47,  63,  80,  95,  111, 127, 191, 255)
    #threschar = ('@', '%', '#', '*', '+', '=', '-', '!', ':', '^', '.')

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

