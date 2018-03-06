import actors.characterObject
import math
class PlayerCharacter(actors.characterObject.Character):
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
    weapon = 0
    headSlot = 0
    chestSlot = 0
    legSlot = 0
    armSlot = 0
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

    def restoreHealth(self, health):
        self.currentLife+=health
        if self.currentLife>self.maxLife:
            self.currentLife=self.maxLife

    def getAttack(self):
        attack = self.baseAttack
        for spell in self.enchantmentList:
            if spell[0]=='attack':
                attack+=spell[1]
        if self.weapon!=0: attack+=self.weapon.value
        return attack

    def getDefense(self):
        defense = self.baseDefense
        for spell in self.enchantmentList:
            if spell[0]=='defense':
                defense+=spell[1]
        if self.headSlot!=0: defense+=self.headSlot.value
        if self.chestSlot!=0: defense+=self.chestSlot.value
        if self.legSlot!=0: defense+=self.legSlot.value
        if self.armSlot!=0: defense+=self.armSlot.value
        return defense

    def dropItem(self, itemIndex):
        if itemIndex>0 and itemIndex<=len(self.itemList):
            item = self.itemList.pop(itemIndex-1)
            print('You dropped the {}'.format(str(item)))
            if item.isEquipped: item.unequip(self)
        else:
            print('That is not an item in your inventory')

    def useItem(self, itemIndex):
        if itemIndex>0 and itemIndex<=len(self.itemList):
            item = self.itemList[itemIndex-1]
            if item.itemType=='consumable':
                print('You used {}'.format(item))
                item.useThis(self)
                self.itemList.pop(itemIndex-1)
                return
            if item.itemType=='weapon':
                if item.isEquipped:
                    print('You removed {}'.format(str(item)))
                    item.unequip(self)
                else:
                    print('You equipped {}'.format(str(item)))
                    item.equip(self)
                return
            if item.itemType=='armor':
                if item.isEquipped:
                    print('You removed {}'.format(str(item)))
                    item.unequip(self)
                else:
                    print('You put on {}'.format(str(item)))
                    item.equip(self)
                return
            print('This is not an item you can use')
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

    def progressTime(self):
        if len(self.enchantmentList)>0: print('You buffs are:')
        for spell in self.enchantmentList:
            spell[2]-=1
            print(' - A buff to {} lasting for {} turns'.format(spell[0], spell[2]))
        stillWorking=True
        while stillWorking:
            a=0
            while a<len(self.enchantmentList) and self.enchantmentList[a][2]>0:
                a+=1
            if a == len(self.enchantmentList):
                stillWorking=False
            else:
                self.enchantmentList.pop(a)

    def move(self, direction):
        target = []
        if direction=='left': target = [self.position[0],self.position[1]-1]
        if direction=='down': target = [self.position[0]+1,self.position[1]]
        if direction=='right': target = [self.position[0],self.position[1]+1]
        if direction=='up': target = [self.position[0]-1,self.position[1]]
        if target!=[]: return target

    def update(self, turnText):
        if turnText[0] == 'wait': return ['wait']
        if len(turnText)<2:
            print('Please add an argument')
            return 'break'
        if turnText[0] == 'move':
            return ['move', self.move(turnText[1])]
        if turnText[0] == 'attack':
            if turnText[1] == 'broad':
                attack = self.attack(turnText[2], True)
                return ['attack', attack[0], attack[1]]
            attack = self.attack(turnText[1])
            return ['attack', attack[0], attack[1]]
