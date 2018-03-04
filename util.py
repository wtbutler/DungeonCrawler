class TextControl():
    mapCache = []
    gameState = 'normal'

    def __init__(self):
        return

    def addMap(self, newMap):
        self.mapCache += [newMap]
