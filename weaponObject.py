class Weapon():
    name = ''
    value = 0
    isEquipped = False

    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.isEquipped = False
        self.itemType = 'weapon'

    def __repr__(self):
        if self.isEquipped: return 'A {} with an attack {} that is currently equipped'.format(self.name, self.value)
        return 'A {} with an attack {}'.format(self.name, self.value)

    def equip(self, player):
        player.weapon = self
        self.isEquipped = True

    def unequip(self, player):
        player.weapon = 0
        self.isEquipped = False
