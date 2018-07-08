import items.itemObject
class Armor(items.itemObject.Item):
    name = ''
    slot = ''
    value = 0
    isEquipped = False
    lowStrengthNames = ['Cloth', 'Goblin',
    medStrengthNames = ['Iron', 'Steel', 'Dwarven', 'Elven',
    highStrengthNames = ['Plate',
    ultStrenthNames = ['Starforged', 'Hellforged',
    headSlotNames = ['Helmet', 'Hat', 'Cap',
    chestSlotNames = ['Armor', 'Shirt', 

    def __init__(self, name, slot, value):
        self.name = name
        self.slot = slot
        self.value = value
        self.isEquipped = False
        self.itemType = 'armor'
        if self.name == 'defaultRandomName': self.name = self.randomName()

    def __repr__(self):
        if self.isEquipped: return 'A {} with an armor rating {} that is currently equipped'.format(self.name, self.value)
        return 'A {} with an armor rating {}'.format(self.name, self.value)

    def randomName(self):
        name = ''
        if self.slot == 'head': name += headSlotNames[]

    def equip(self, player):
        if self.slot == 'head': player.headSlot = self
        if self.slot == 'chest': player.chestSlot = self
        if self.slot == 'legs': player.legSlot = self
        if self.slot == 'arms': player.armSlot = self
        self.isEquipped = True

    def unequip(self, player):
        if self.slot == 'head': player.headSlot = 0
        if self.slot == 'chest': player.chestSlot = 0
        if self.slot == 'legs': player.legSlot = 0
        if self.slot == 'arms': player.armSlot = 0
        self.isEquipped = False
