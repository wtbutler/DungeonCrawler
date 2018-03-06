class DungeonMap():
    name = ""
    mapCoordinateList = []
    actorList = []

    def __init__(self, mapListFromReader):
        self.name = mapListFromReader.pop(-1)
        self.mapCoordinateList = mapListFromReader
        self.actorList = []
        self.objectList = []

    def tileAt(self, location):
        return self.mapCoordinateList[location[0]][location[1]]

    def setConnection(self, connectionInfo):
        self.tileAt(connectionInfo[0][1]).setConnection(connectionInfo[1][0], connectionInfo[1][1])

    def addCreature(self, creature):
        location = creature.position
        if self.tileAt(location).canPlace():
            self.actorList+=[creature]
            self.tileAt(location).actor=creature
        else:
            print("not possible")

    def addObject(self, newObject):
        location = newObject.position
        if self.tileAt(location).canPlace():
            self.objectList+=[newObject]
            self.tileAt(location).actor=newObject
        else:
            print("not possible")
