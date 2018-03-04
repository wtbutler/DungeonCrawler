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
        if len(self.items)==0:
            print(' - Nothing!')
            return
        for i in range(len(self.items)):
            print(' - {} {}'.format(i+1, self.items[i]))

    def take(self, itemIndex):
        if len(self.items)==0: return 'breakThis'
        item = self.items.pop(itemIndex-1)
        print('You picked up {}'.format(item))
        self.giveInfo(took=True)
        return item
