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
imOut.save(imName + "_preTH.png")
pixOut = imOut.load()
i = 0
j = 0
while j < dimOut:
    while i < dimOut:
        val = pixOut[i,j]
        if val[1] == 0:
            pixOut[i,j] = (255, 0)
        elif val[0] <= 31:
            pixOut[i,j] = (16, 255)
        elif val[0] >= 32 and val[0] <= 63:
            pixOut[i,j] = (48, 255)
        elif val[0] >= 64 and val[0] <= 95:
            pixOut[i,j] = (80, 255)
        elif val[0] >= 96 and val[0] <= 127:
            pixOut[i,j] = (112, 255)
        elif val[0] >= 128 and val[0] <= 159:
            pixOut[i,j] = (144, 255)
        elif val[0] >= 160 and val[0] <= 191:
            pixOut[i,j] = (176, 255)
        elif val[0] >= 192 and val[0] <= 223:
            pixOut[i,j] = (208, 255)
        elif val[0] >= 224:
            pixOut[i,j] = (240, 255)
        i+=1
    i=0
    j+=1

imOut.save(imName + "_final.png")

imOut.close()
