class Item():
    name = ""
    # Eg. Weapon, Armor, Misc
    itemType = ""
    # Eg. Head, Body, Feet, Arms, None
    slot = ""
    # Eg. Attack, Defense, Health, Time
    modifier = ""
    # How much the modifier changes
    value = 0

    def __init__(self, setType, setSlot, setModifier, setValue):
        self.name = setName
        self.itemType = setType
        self.slot = setSlot
        self.modifier = setModifier
        self.value = setValue
