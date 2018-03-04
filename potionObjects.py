import itemObject
class Consumable(itemObject.Item):
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

    def __str__(self):
        if duration==None: return 'A {} that increases {} by {}'.format(self.name, self.attriute, self.value)
        return 'A {} that boosts {} by {} for {}'.format(self.name, self.attriute, self.value, self.duration)

    def drinkThis(self, player):
        if self.duration==None:
            if self.attribute=='currentLife':
                player.currentLife+=self.value
            if self.attribute=='maxLife':
                player.maxLife+=self.value
            if self.attribute=='baseAttack':
                player.baseAttack+=self.value
            if self.attriute=='baseDefense':
                player.baseDefense+=self.value
            if self.attribute=='experience':
                player.gainExperience(self.value)
            return
        player.enchantmentList += [self.attriute, self.value, self.duration]
