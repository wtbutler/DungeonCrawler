class TextControl():
    mapCache = []
    gameState = 'normal'
    chest = 0

    def __init__(self):
        return

    def addMap(self, newMap):
        self.mapCache += [newMap]
