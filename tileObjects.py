import tile
class FloorTile(tile.Tile):
    actorList = []
    def __init__(self):
        self.actorList = []
        self.icon = "  "

    def attack(self, damage):
        self.icon = "//"
        self.actor.takeDamage(damage)
        self.icon = "  "

    def isEmpty(self):
        return len(self.actorList)==0
    def canPlace(self):
        return len(self.actorList)==0

class WallTile(tile.Tile):
    def __init__(self, myicon):
        self.icon = myicon
    def isEmpty(self):
        return False
    def canPlace(self):
        return False

class DoorTile(tile.Tile):
    connection = []
    def __init__(self):
        self.init = "--"
        self.connection = []
    def setConnection(self, destMapName, destMapCoordinates):
        self.connection = [destMapName, destMapCoordinates]
    def isEmpty(self):
        return True
    def canPlace(self):
        return False
