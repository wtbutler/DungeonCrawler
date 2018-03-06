class Item():
    name = ""
    isEquipped = False
    itemType = ''

    def __init__(self, setName):
        self.name = setName
        self.isEquipped = False

    def __str__(self):
        return self.name
