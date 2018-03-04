import characterObject
import math
class PlayerCharacter(characterObject.Character):
    icon = "()"
    name = "Neft"
    position= [0,0]
    maxLife = 20
    currentLife = 20
    baseAttack = 5
    baseDefense = 5
    level=1
    experience=0
    # Head, Torso, Legs, Arms
    armorList = []
    weapon = ''
    itemList = []
    enchantmentList = []

    def __init__(self, positionx, positiony):
        self.position[0] = positionx
        self.position[1] = positiony

    def giveInfo(self):
        print('It\'s you, {}!'.format(self.name))

    def takeDamage(self, damage):
        actualDamage = math.ceil(damage*(100-self.getDefense())/100)
        print('You took {} damage'.format(actualDamage))
        self.currentLife -= actualDamage

    def getAttack(self):
        attack = self.baseAttack
        for spell in self.enchantmentList:
            if spell[0]=='attack':
                attack+=spell[1]
        return attack

    def getDefense(self):
        defense = self.baseDefense
        for spell in self.enchantmentList:
            if spell[0]=='defense':
                defense+=spell[1]
        return defense

    def dropItem(self, itemIndex):
        if itemIndex>0 and itemIndex<=len(self.itemList):
            print('You dropped {}'.format(self.itemList.pop(itemIndex-1)))
        else:
            print('That is not an item in your inventory')

    def useItem(self, itemIndex):
        if itemIndex>0 and itemIndex<=len(self.itemList):
            if self.itemList[itemIndex-1].itemType=='consumable':
                self.itemList[itemIndex-1].useThis(self)
            else:
                print('Please try to use a consumable item')
        else:
            print('That is not an item in your inventory')

    def attack(self, direction, broad=False):
        damage = self.getAttack()
        tileList = []
        if direction=='left': tileList += [[self.position[0],self.position[1]-1]]
        if direction=='down': tileList += [[self.position[0]+1,self.position[1]]]
        if direction=='right': tileList += [[self.position[0],self.position[1]+1]]
        if direction=='up': tileList += [[self.position[0]-1,self.position[1]]]
        if broad:
            damage*=.33
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
    def equip(self, item):
        if item.itemType=="Weapon":
            self.weapon = item
        if item.itemType=="Armor":
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
        if turnText[0] == 'move':
            return ['move', self.move(turnText[1])]
        if turnText[0] == 'attack':
            if turnText[1] == 'broad':
                attack = self.attack(turnText[2], True)
                return ['attack', attack[0], attack[1]]
            attack = self.attack(turnText[1])
            return ['attack', attack[0], attack[1]]
