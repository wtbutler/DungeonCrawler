import random as r
import generalObject as genO
import math
class Character(genO.GeneralObject):
    name = "default character name"
    maxLife = 0
    currentLife = 0
    baseAttack = 0
    baseDefence = 0
    level = 0
    # reference -     up    right down  left
    availableSides = [True, True, True, True]
    rand = r.Random()

    def teleport(self, targetPoint):
        self.position[0] = targetPoint[0]
        self.position[1] = targetPoint[1]

    def attack(self, target):
        return

    def takeDamage(self, damage):
        self.currentLife -= math.ceil(damage*(100-self.defense)/100)

    def findDistance(self, pos2, distType = "absolute"):
        if distType == "absolute": return ((self.position[0]-pos2[0])*(self.position[0]-pos2[0])+(self.position[1]-pos2[1])*(self.position[1]-pos2[1]))
        if distType == "turns": return abs(self.position[0]-player.position[0])+abs(self.position[1]-player.position[1])-1

    def update(self, currentMap, actorList, turnText):
        availableSides = self.testWalls(currentMap.mapCoordinateList)
        return ""

    def updateInfo(self):
        self.info = [self.name, self.position, self.maxLife, self.currentLife, self.level, self.icon]
