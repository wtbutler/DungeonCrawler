import generalObject as genO
class Chest(genO.GeneralObject):
    icon = "(]"
    name = "chest"
    poisition = []
    
    def __init__(self, position, items=[]):
        self.items = items
        self.position = position
        self.info = [self.name, position, len(self.items), self.icon]
