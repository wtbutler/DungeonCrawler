import tile
class FloorTile(tile.Tile):
    actorList = []
    def __init__(self):
        self.actorList = []
        self.icon = "  "

    def attack(self, damage):
        self.icon = "//"
        for actor in self.actorList:
            actor.takeDamage(damage)
        self.icon = "  "


class WallTile(tile.Tile):
    def __init__(self, myicon):
        self.icon = myicon


class DoorTile(tile.Tile):
    connection = []
    def __init__(self):
        self.init = "--"
        self.connection = []
    def setConnection(self, destMapName, destMapCoordinates):
        self.connection = [destMapName, destMapCoordinates]
