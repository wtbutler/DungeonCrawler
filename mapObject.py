import tile
class DungeonMap():
    name = ""
    mapCoordinateList = []
    mapInfo = []
    actorList = []
    objectList = []

    def __init__(self, mapListFromReader):
        self.mapInfo = mapListFromReader.pop(-1)
        print(self.mapInfo)
        self.name = self.mapInfo[0]
        self.mapCoordinateList = mapListFromReader
        self.actorList = []
        self.objectList = []

    def tileAt(self, location):
        return self.mapCoordinateList[location[0]][location[1]]

    def setConnection(self, connectionInfo):
        self.tileAt(connectionInfo[0][1]).setConnection(connectionInfo[1][0], connectionInfo[1][1])

    def addCreature(self, location, creature):
        if self.tileAt(location).canPlace():
            self.actorList+=[creature]
            self.tileAt(location).actor=creature
        else:
            print("not possible")
