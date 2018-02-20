import characterObject
import chestObject
import math
class Monster(characterObject.Character):
    icon = ":["
    name = "default monster name"
    maxLifeModifier = 5
    baseAttack = 5
    baseDefence = 5
    level = 0
    items = []

    def __init__(self, name, position, level, health = -1, items = []):
        self.name = name
        self.level = level
        self.position = position
        self.maxLife = self.maxLifeModifier * level
        self.currentLife = self.maxLife
        self.items = items
        if health != -1:
            self.currentLife = health
            if self.currentLife>self.maxLife: self.maxLife = health

    def attack(self, target):
        if self.rand.random()<.8:
            damageDone = int(self.baseAttack*(100-target.baseDefence)/100)
            print("You took {damage} damage!".format(damage = damageDone))
            target.takeDamage(damageDone)
        else:
            print("The monster missed!")

    def death(self):
        return chestObject.Chest(self.position, items = self.items)

    def moveRandom(self, availableSides):
        options = [0]
        for side in range(len(availableSides)):
            if availableSides[side]:
                options+=[side+1]
        choice = options[int(self.rand.random()*(len(options)-.5)+.5)]
        if choice == 1:
            self.position = [self.position[0], self.position[1]-1]
        if choice == 2:
            self.position = [self.position[0]+1, self.position[1]]
        if choice == 3:
            self.position = [self.position[0], self.position[1]+1]
        if choice == 4:
            self.position = [self.position[0]-1, self.position[1]]


# reference - available sides = [up,right,down,left]
    def update(self, currentMap, actorList, turnText):
        availableSides = self.testWalls(currentMap.mapCoordinateList)
        distance = self.findDistance(actorList[0].position)
        if distance<=9 and distance>2:
            dx = actorList[0].position[0]-self.position[0]
            dy = actorList[0].position[1]-self.position[1]
            # Checks if right and left are available and if it has priority to move in that direction
            if dx!=0 and (abs(dx)>=abs(dy) and dx>0 and availableSides[1]) or (abs(dx)>=abs(dy) and dx<0 and availableSides[3]):
                self.position[0]+=int(math.copysign(1,dx))
            # Checks if it should move up or down
            elif dy!=0 and (dy<0 and availableSides[0]) or (dy>0 and availableSides[2]):
                self.position[1]+=int(math.copysign(1,dy))
            # Checks if it should move right or left again in case it couldn't move left or right
            elif (dx>0 and availableSides[1]) or (dx<0 and availableSides[3]):
                self.position[0]+=int(math.copysign(1,dx))
            # Reaches here if it cannot move closer to the actorList[0] but still sees it,
            else:
                self.moveRandom(availableSides)
        elif distance<=2:
            self.attack(actorList[0])
        else:
            self.moveRandom(availableSides)
