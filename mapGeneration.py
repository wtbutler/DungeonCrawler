import os, sys
from PIL import Image
from PIL import ImageDraw

def makeDungeonMap():
    imageName = input("image name? ")
    inputImage = Image.open("maps\\"+imageName+".png")
    mapImage = Image.new('RGB', inputImage.size,color = 0xffffff)
    mapPix = mapImage.load()
    pix1 = inputImage.load()
    xLen = mapImage.size[0]
    yLen = mapImage.size[1]

    #
    # The fill color is black
    # Any moveable space should be filled white
    # Use rectangles to form rooms and corridors 
    #

    for x in range(xLen):
        for y in range(yLen):
            mapImage.putpixel((x,y), pix1[x,y])
    try:
        os.remove("maps\\"+imageName + ".png")
    except:
        pass
    mapImage.save("maps\\"+imageName+".png")

#makeDungeonMap(sys.argv[1])
makeDungeonMap()
