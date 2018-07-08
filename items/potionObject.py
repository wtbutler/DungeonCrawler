import items.itemObject
class Consumable(items.itemObject.Item):
    name = ''
    itemType=''
    attribute = ''
    value = 0
    duration = None

    def __init__(self, name, attribute, value, duration=None):
        self.name=name
        self.itemType = 'consumable'
        self.attribute = attribute
        self.value = value
        self.duration = duration
        if self.name == 'defaultRandomName': self.name = self.randomName()

    def __repr__(self):
        if self.duration==None: return 'A {} that increases {} by {}'.format(self.name, self.attribute, self.value)
        return 'A {} that boosts {} by {} for {} turns'.format(self.name, self.attribute, self.value, self.duration)

    def useThis(self, player):
        if self.duration==None:
            if self.attribute=='currentLife':
                player.restoreHealth(self.value)
            if self.attribute=='maxLife':
                player.maxLife+=self.value
                player.restoreHealth(value)
            if self.attribute=='baseAttack':
                player.baseAttack+=self.value
            if self.attribute=='baseDefense':
                player.baseDefense+=self.value
            if self.attribute=='experience':
                player.gainExperience(self.value)
            return
        player.enchantmentList += [[self.attribute, self.value, self.duration]]
