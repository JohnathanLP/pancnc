from PIL import Image
imName = raw_input("Image name (without extension):") 
imIn = Image.open(imName + ".png")
pixIn = imIn.load()
print "Image loaded successfully!"
wide, high = imIn.size
print wide, high
print imIn.mode

imBW = Image.new("RGBA", (wide,high), "white")
pixBW = imBW.load()

i = 0
j = 0
while j < high:
  while i < wide: 
    pixBW[i,j] = pixIn[i,j]
    ave = pixIn[i,j][0]+pixIn[i,j][1]+pixIn[i,j][2]
    ave /= 3
    pixBW[i,j] = (ave,ave,ave, pixIn[i,j][3])
    i+=1
  i=0
  j+=1

imBW.save(imName + "_BW.png")

dimOut = 32

#imScaled = Image.new("RGBA", (dimOut,dimOut), "white")
imScaled = imBW.resize((dimOut,dimOut))
imScaled.save(imName + "_scaled.png")

imL = imIn.convert("L")
imL.save(imName + "_L.png")

imIn.close()
imBW.close()
imScaled.close()
