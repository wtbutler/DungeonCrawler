import tile
class FloorTile(tile.Tile):
    actor = 0
    def __init__(self):
        self.actor = 0
        self.icon = "  "
        self.attacked = False
    def __str__(self):
        if self.attacked:
            return '//'
        if not(self.isEmpty()):
            return self.actor.icon
        return self.icon

    def attack(self, damage):
        self.attacked=True
        self.actor.takeDamage(damage)
    def default(self):
        self.attacked=False
    def isEmpty(self):
        return (self.actor==0)
    def canPlace(self):
        return (self.actor==0)
    def emptyThis(self):
        self.actor = 0
    def tileType(self):
        return 'floor'

class WallTile(tile.Tile):
    def __init__(self, myicon):
        self.icon = myicon
    def isEmpty(self):
        return False
    def canPlace(self):
        return False
    def tileType(self):
        return 'wall'

class DoorTile(tile.Tile):
    connection = []
    def __init__(self):
        self.icon = "--"
        self.connection = []
    def setConnection(self, destMapName, destMapCoordinates):
        self.connection = [destMapName, destMapCoordinates]
    def getConnection(self):
        return self.connection
    def tileType(self):
        return 'door'
    def isEmpty(self):
        return True
    def canPlace(self):
        return False
