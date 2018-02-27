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

    def giveInfo(self):
        print('A wooden chest that contains:')
        if len(self.items)==0:
            print(' - Nothing!')
            return
        for i in range(len(self.items)):
            print(' - {} {}'.format(i, self.items[i]))

    def take(self, itemIndex):
        item = self.items.pop(itemIndex)
        self.giveInfo
        return item
