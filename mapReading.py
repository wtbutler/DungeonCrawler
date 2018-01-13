import os,sys
from PIL import Image

def getMapFromImage(path, image):
    
    inputImage = Image.open(path+image)
    mapPix = inputImage.load()
    
    xLen = inputImage.size[0]
    yLen = inputImage.size[1]
    emptyFloor = (255,255,255)
    door = (255,0,0)
    infoList = [image[:-4]]
    mapToReturn = []
    for y in range(yLen):
        tempArray = []
        for x in range(xLen):
            tempArray+=[""]
        mapToReturn += [tempArray]
    for x in range(xLen):
        for y in range(yLen):
            tile = "  "
            if mapPix[x,y] != emptyFloor:
                up = False
                down = False
                right = False
                left = False
                neighbors = 0
                if  mapPix[x,y-1]!=emptyFloor:
                    up = True
                    neighbors+=1
                if mapPix[x,y+1]!=emptyFloor:
                    down = True
                    neighbors+=1
                if mapPix[x-1,y]!=emptyFloor:
                    left = True
                    neighbors+=1
                if mapPix[x+1,y]!=emptyFloor:
                    right = True
                    neighbors+=1
                if up and down: tile = "||"
                elif left and right: tile = "=="
                else: tile = "##"
            if mapPix[x,y] == door:
                tile = "--"
                infoList+=[(x,y)]
            mapToReturn[y][x] = tile
    return mapToReturn+[infoList]
