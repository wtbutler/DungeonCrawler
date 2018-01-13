class DungeonMap():
    name = ""
    mapCoordinateList = []
    mapInfo = []
    connectionPoints = []
    connections = []
    enemyList = []
    objectList = []

    def __init__(self, mapListFromReader):
        self.mapInfo = mapListFromReader.pop(-1)
        self.name = self.mapInfo[0]
        self.connectionPoints = self.mapInfo[1:]
        self.mapCoordinateList = mapListFromReader
        self.connections = []
        self.enemyList = []
        self.objectList = []

    def setConnections(self, listOfConnections):
        self.connections = listOfConnections
