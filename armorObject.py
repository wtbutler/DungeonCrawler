class Armor():
    name = ''
    slot = ''
    value = 0
    isEquipped = False

    def __init__(self, name, slot, value):
        self.name = name
        self.slot = slot
        self.value = value
        self.isEquipped = False
        self.itemType = 'armor'

    def __repr__(self):
        if self.isEquipped: return 'A {} with an armor rating {} that is currently equipped'.format(self.name, self.value)
        return 'A {} with an armor rating {}'.format(self.name, self.value)

    def equip(self, player):
        if self.slot=='head': player.headSlot = self
        if self.slot=='chest': player.chestSlot = self
        if self.slot=='legs': player.legSlot = self
        if self.slot=='arms': player.armSlot = self
        self.isEquipped = True

    def unequip(self, player):
        if self.slot=='head': player.headSlot = 0
        if self.slot=='chest': player.chestSlot = 0
        if self.slot=='legs': player.legSlot = 0
        if self.slot=='arms': player.armSlot = 0
        self.isEquipped = False
