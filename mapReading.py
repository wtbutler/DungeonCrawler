import os,sys
from PIL import Image
import tileObjects

def getMapFromImage(path, image):

    inputImage = Image.open(path+image)
    mapPix = inputImage.load()

    xLen = inputImage.size[0]
    yLen = inputImage.size[1]
    emptyFloor = (255,255,255)
    door = (255,0,0)
    wall = (0,0,0)
    mapName = image[:-4]
    mapToReturn = []
    for y in range(yLen):
        tempArray = []
        for x in range(xLen):
            tempArray+=[""]
        mapToReturn += [tempArray]
    for x in range(xLen):
        for y in range(yLen):
            tile = "  "
            if mapPix[x,y] == emptyFloor: mapToReturn[y][x] = tileObjects.FloorTile()
            if mapPix[x,y] == wall:
                up = False
                down = False
                right = False
                left = False
                neighbors = 0
                if  mapPix[x,y-1]==wall:
                    up = True
                    neighbors+=1
                if mapPix[x,y+1]==wall:
                    down = True
                    neighbors+=1
                if mapPix[x-1,y]==wall:
                    left = True
                    neighbors+=1
                if mapPix[x+1,y]==wall:
                    right = True
                    neighbors+=1
                if neighbors>=3: tile = "##"
                elif up and down: tile = "||"
                elif left and right: tile = "=="
                else: tile = "##"
                mapToReturn[y][x] = tileObjects.WallTile(tile)
            if mapPix[x,y] == door:
                tile = "--"
                mapToReturn[y][x] = tileObjects.DoorTile()
    print(mapName)
    return mapToReturn+[mapName]
