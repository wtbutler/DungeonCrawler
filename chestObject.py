import generalObject as genO
class Chest(genO.GeneralObject):
    icon = "(]"
    name = "chest"
    poisition = []
    items = []

    def __init__(self, position, name='chest', items=[]):
        self.items = items
        self.position = position
        if name!='chest': self.name = 'chest from {}'.format(name)

    def giveInfo(self, took=False):
        if took:
            print('The chest now contains:')
        else:
            print('A wooden chest that contains:')
        for i in range(len(self.items)):
            print(' - {} {}'.format(i+1, self.items[i]))
        print(' - {} {}'.format(len(self.items)+1, 'Destroy this chest'))

    def take(self, itemIndex, takeAll=False):
        if itemIndex<=0 or itemIndex>(len(self.items)+1): return
        if itemIndex==(len(self.items)+1): return 'breakThis'
        item = self.items.pop(itemIndex-1)
        print('You picked up {}'.format(item))
        if not(takeAll): self.giveInfo(took=True)
        return item
