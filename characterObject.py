import random as r
import generalObject as genO
class Character(genO.GeneralObject):
    name = "default character name"
    maxLife = 0
    currentLife = 0
    baseAttack = 0
    baseDefence = 0
    level = 0
    # reference -     up    right down  left
    availableSides = [True, True, True, True]
    walkable = ["  "]
    rand = r.Random()

    def teleport(self, targetPoint):
        self.position[0] = targetPoint[0]
        self.position[1] = targetPoint[1]

    def attack(self, target):
        return

    def takeDamage(self, damage):
        self.currentLife -= damage

    def findDistance(self, pos2, distType = "absolute"):
        if distType == "absolute": return ((self.position[0]-pos2[0])*(self.position[0]-pos2[0])+(self.position[1]-pos2[1])*(self.position[1]-pos2[1]))
        if distType == "turns": return abs(self.position[0]-player.position[0])+abs(self.position[1]-player.position[1])-1

    def testWalls(self, currentMap, actorList):
        testables = [currentMap[self.position[1]-1][self.position[0]],
                     currentMap[self.position[1]][self.position[0]+1],
                     currentMap[self.position[1]+1][self.position[0]],
                     currentMap[self.position[1]][self.position[0]-1]]
        for actor in actorList:
            if self.findDistance(actor.position) == 1:
                xDist = self.position[0]-actor.position[0]
                yDist = self.position[1]-actor.position[1]
                if xDist == 1:
                    testables[3] = actor.icon
                if xDist == -1:
                    testables[1] = actor.icon
                if yDist == -1:
                    testables[2] = actor.icon
                if yDist == 1:
                    testables[0] = actor.icon
        toReturn = [False, False, False, False]
        for i in range(len(testables)):
            for test in self.walkable:
                if testables[i] == test:
                    toReturn[i] = True
        return toReturn

    def update(self, currentMap, actorList, turnText):
        availableSides = self.testWalls(currentMap.mapCoordinateList)
        return ""

    def updateInfo(self):
        self.info = [self.name, self.position, self.maxLife, self.currentLife, self.level, self.icon]
