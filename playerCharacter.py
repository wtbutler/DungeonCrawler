import characterObject
class PlayerCharacter(characterObject.Character):
    icon = "()"
    name = "Neft"
    position= [0,0]
    maxLife = 20
    currentLife = 20
    walkable = ["  ","--"]
    baseAttack = 2
    attack = 10
    baseDefence = 5
    defense = 10
    currentWeapon = ""
    currentArmor = ""
    # Head, Torso, Legs, Arms
    armorList = []
    # Rh, Lh
    weapon = ""
    itemList = []

    def __init__(self, positionx, positiony):
        self.position[0] = positionx
        self.position[1] = positiony
        self.defense = self.baseDefence
        self.attack = self.baseAttack

    def attack(self, target, currentActors):
        if self.rand.random()<.9:
            damageDone = int((self.baseAttack)*(100-target.baseDefence)/100)
            target.takeDamage(damageDone)
            print("Did {} damage!".format(damageDone))
        else:
            print("You missed!")

    def loadFromInfo(self):
        self.name, self.position, self.maxLife, self.currentLife, self.level, self.icon = self.info

    def equip(self, item):
        if item.itemType=="Weapon":
            self.weapon = item
            self.attack = self.baseAttack+self.weapon.value
        elif item.itemType=="Armor":
            if item.slot=="Head":
                if self.armorList[0]:
                    print('do Nothing')
                self.armorList[0]=item
            if item.slot=="Torso":
                self.armorList[1]=item
            if item.slot=="Legs":
                self.armorList[2]=item
            if item.slot=="Arms":
                self.armorList[3]=item
        else:
            print("Please try to equip a valid item.")

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
            string = 'move '+self.position+' '+turntext[1]
            print(string)
            return string
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
