import tile
class FloorTile(tile.Tile):
    actor = 0
    def __init__(self):
        self.actor = 0
        self.icon = "  "
        self.attacked = False
        self.type = 'floor'
    def __str__(self):
        if self.attacked:
            return '//'
        if not(self.isEmpty()):
            return self.actor.icon
        return self.icon
    def attack(self, damage):
        print('actor taking damage: {}'.format(self.actor))
        self.attacked=True
        if self.actor!=0: self.actor.takeDamage(damage)
    def default(self):
        self.attacked=False
    def isEmpty(self):
        return (self.actor==0)
    def canPlace(self):
        return (self.actor==0)
    def emptyThis(self):
        self.actor = 0
    def check(self):
        if self.isEmpty():
            print('A piece of empty floor')
        else:
            self.actor.giveInfo()

class WallTile(tile.Tile):
    def __init__(self, myicon):
        self.icon = myicon
        self.type = 'wall'
    def isEmpty(self):
        return False
    def canPlace(self):
        return False
    def check(self):
        print('A very solid wall!')

class DoorTile(tile.Tile):
    connection = []
    def __init__(self):
        self.icon = "--"
        self.connection = []
        self.type = 'door'
    def setConnection(self, destMapName, destMapCoordinates):
        self.connection = [destMapName, destMapCoordinates]
    def getConnection(self):
        return self.connection
    def isEmpty(self):
        return True
    def canPlace(self):
        return False
    def check(self):
        print('A door to another room')
