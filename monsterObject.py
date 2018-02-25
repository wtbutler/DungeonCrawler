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
        self.icon = ":["
        self.level = level
        self.position = position
        self.maxLife = self.maxLifeModifier * level
        self.currentLife = self.maxLife
        self.items = items
        if health != -1:
            self.currentLife = health
            if self.currentLife>self.maxLife: self.maxLife = health

    def attack(self, playerPos, availableSides):
        tileList = []
        damage = self.baseAttack
        xDiff = playerPos[1]-self.position[1]
        yDiff = playerPos[0]-self.position[0]
        if xDiff!=0 and yDiff==0:
            tileList+=[[self.position[0], self.position[1]+int(math.copysign(1,xDiff))]]
            return [damage, tileList]
        if xDiff==0 and yDiff!=0:
            tileList+=[[self.position[0]+int(math.copysign(1,yDiff)), self.position[1]]]
            return [damage, tileList]
        damage *= .5
        if (xDiff>0 and availableSides[1]) or (xDiff<0 and availableSides[3]):
            tileList+=[[self.position[0], self.position[1]+int(math.copysign(1,xDiff))]]
            tileList+=[[self.position[0]+1, self.position[1]+int(math.copysign(1,xDiff))]]
            tileList+=[[self.position[0]-1, self.position[1]+int(math.copysign(1,xDiff))]]
        elif (yDiff>0 and availableSides[2]) or (yDiff<0 and availableSides[0]):
            tileList+=[[self.position[0]+int(math.copysign(1,yDiff)), self.position[1]]]
            tileList+=[[self.position[0]+int(math.copysign(1,yDiff)), self.position[1]+1]]
            tileList+=[[self.position[0]+int(math.copysign(1,yDiff)), self.position[1]-1]]
        return [damage, tileList]

    def death(self):
        return chestObject.Chest(self.position, items = self.items)

    def moveRandom(self, availableSides):
        options = [0]
        for side in range(len(availableSides)):
            if availableSides[side]:
                options+=[side+1]
        choice = options[int(self.rand.random()*(len(options)-.5)+.5)]
        if choice == 1:
            return [self.position[0]-1, self.position[1]]
        if choice == 2:
            return [self.position[0], self.position[1]+1]
        if choice == 3:
            return [self.position[0]+1, self.position[1]]
        if choice == 4:
            return [self.position[0], self.position[1]-1]
        return self.position

    def moveToPlayer(self, playerPos, availableSides):
        dx = playerPos[1]-self.position[1]
        dy = playerPos[0]-self.position[0]
        target = [0,0]
        # Checks if right and left are available and if it has priority to move in that direction
        if abs(dx)>=abs(dy) and ((dx>0 and availableSides[1]) or (dx<0 and availableSides[3])):
            target[1]+=int(math.copysign(1,dx))
        # Checks if it should move up or down
        elif (dy<0 and availableSides[0]) or (dy>0 and availableSides[2]):
            target[0]+=int(math.copysign(1,dy))
        # Checks if it should move right or left again in case it couldn't move left or right
        elif (dx>0 and availableSides[1]) or (dx<0 and availableSides[3]):
            target[1]+=int(math.copysign(1,dx))
        # Reaches here if it cannot move closer to the actorList[0] but still sees it,
        else:
            return self.moveRandom(availableSides)
        return [self.position[0]+target[0], self.position[1]+target[1]]
        # return 'move'+direction

    # reference - available sides = [up,right,down,left]
    def update(self, availableSides, playerPos):
        distance = self.findDistance(playerPos)
        if distance<=9 and distance>2:
            return ['move', self.moveToPlayer(playerPos, availableSides)]
        elif distance<=2:
            attack = self.attack(playerPos, availableSides)
            return ['attack', attack[0], attack[1]]
            # return 'attack'+direction
        else:
            return ['move', self.moveRandom(availableSides)]
            # return 'move'+direction
