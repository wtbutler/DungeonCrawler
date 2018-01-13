import characterObject
class PlayerCharacter(characterObject.Character):
    icon = "()"
    name = "Neft"
    position= [0,0]
    maxLife = 20
    currentLife = 20
    walkable = ["  ","--"]
    baseAttack = 2
    baseDefence = 5
    currentWeapon = ""
    currentArmor = ""
    armorList = []
    weaponList = []
    miscItemList = []
    itemList = [armorList, weaponList, miscItemList]

    def __init__(self, positionx, positiony):
        self.position[0] = positionx
        self.position[1] = positiony

    def attack(self, target, currentActors):
        if self.rand.random()<.9:
            damageDone = int(self.baseAttack*(100-target.baseDefence)/100)
            target.takeDamage(damageDone)
            print("Did {} damage!".format(damageDone))
        else:
            print("You missed!")

    def loadFromInfo(self):
        self.name, self.position, self.maxLife, self.currentLife, self.level, self.icon = self.info

    def move(self, currentMap, actorList, direction):
        availableSides = self.testWalls(currentMap.mapCoordinateList, actorList)
        dungeonMap = currentMap.mapCoordinateList
        if direction == "down":
            if availableSides[2] == True:
                self.position[1]+=1
            else:
                print("bump")
        elif direction == "right":
            if availableSides[1] == True:
                self.position[0]+=1
            else:
                print("bump")
        elif direction == "left":
            if availableSides[3] == True:
                self.position[0]-=1
            else:
                print("bump")
        elif direction == "up":
            if availableSides[0] == True:
                self.position[1]-=1
            else:
                print("bump")

    def update(self, currentMap, actorList, turnText):
        if turnText[0] == 'move':
            self.move()
        if turnText[0] == 'attack':
            try:
                if self.findDistance(self.currentActors[int(self.turnText[1])].position)<4:
                    self.attack(self.currentActors[int(self.turnText[1])], self.currentActors)
                else:
                    print("Too far away!")
                    self.textType = 'pass'
            except (ValueError, IndexError):
                print("invalid enemy")
                self.textType = 'pass'
