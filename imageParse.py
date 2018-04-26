from PIL import Image
imName = raw_input("Image name (without extension):") 
imIn = Image.open(imName + ".png")
pixIn = imIn.load()
print "Image loaded successfully!"
wide, high = imIn.size
print wide, high
print imIn.mode

imOut = Image.new("RGBA", (wide,high), "white")
pixOut = imOut.load()

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

dimOut = 32
imOut = imOut.resize((dimOut,dimOut))
imOut = imOut.convert("LA")
#imOut.save(imName + "_preTH.png")

pixOut = imOut.load()
#threshold = (0,31,63,95,127,159,191,223,255)
threshold = (0,15,31,47,63,80,95,111,127,191,255)
i = 0
j = 0
while j < dimOut:
    while i < dimOut:
        val = pixOut[i,j]
        if val[1] == 0:
            pixOut[i,j] = (255,0)
        else:
            for thresh in threshold:
                if val[0] < thresh:
                    pixOut[i,j] = (thresh, 255)
                    break
        i+=1
    i=0
    j+=1

imOut.save(imName + "_final.png")

imOut.close()
