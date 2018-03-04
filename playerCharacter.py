import characterObject
class PlayerCharacter(characterObject.Character):
    icon = "()"
    name = "Neft"
    position= [0,0]
    maxLife = 20
    currentLife = 20
    baseAttack = 5
    baseDefence = 5
    # Head, Torso, Legs, Arms
    armorList = []
    weapon = ''
    itemList = []

    def __init__(self, positionx, positiony):
        self.position[0] = positionx
        self.position[1] = positiony

    def giveInfo(self):
        print('It\'s you, {}!'.format(self.name))

    def attack(self, direction, broad=False):
        damage = self.baseAttack
        tileList = []
        if direction=='left': tileList += [[self.position[0],self.position[1]-1]]
        if direction=='down': tileList += [[self.position[0]+1,self.position[1]]]
        if direction=='right': tileList += [[self.position[0],self.position[1]+1]]
        if direction=='up': tileList += [[self.position[0]-1,self.position[1]]]
        if broad:
            damage*=.5
            if direction=='left':
                tileList += [[self.position[0]+1,self.position[1]-1]]
                tileList += [[self.position[0]-1,self.position[1]-1]]
            if direction=='down':
                tileList += [[self.position[0]+1,self.position[1]+1]]
                tileList += [[self.position[0]+1,self.position[1]-1]]
            if direction=='right':
                tileList += [[self.position[0]+1,self.position[1]+1]]
                tileList += [[self.position[0]-1,self.position[1]+1]]
            if direction=='up':
                tileList += [[self.position[0]-1,self.position[1]+1]]
                tileList += [[self.position[0]-1,self.position[1]-1]]
        if tileList!=[]: return [damage, tileList]
        return ['error', 'error']

    def addItem(self, item):
        self.itemList += [item]
        print('You picked up {}'.format(item))
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

    def move(self, direction):
        target = []
        if direction=='left': target = [self.position[0],self.position[1]-1]
        if direction=='down': target = [self.position[0]+1,self.position[1]]
        if direction=='right': target = [self.position[0],self.position[1]+1]
        if direction=='up': target = [self.position[0]-1,self.position[1]]
        if target!=[]: return target

    def update(self, turnText):
        print('turnText in Player: {}'.format(turnText))
        if turnText[0] == 'move':
            return ['move', self.move(turnText[1])]
        if turnText[0] == 'attack':
            if turnText[1] == 'broad':
                attack = self.attack(turnText[2], True)
                return ['attack', attack[0], attack[1]]
            attack = self.attack(turnText[1])
            return ['attack', attack[0], attack[1]]
