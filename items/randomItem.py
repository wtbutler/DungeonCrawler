import items.itemObject
import items.armorObject
import items.potionObject
import items.weaponObject
import random as r

armorSlots = [ 'head', 'chest', 'legs', 'arms' ]
consumableTypes = [ 'currentLife', 'attack', 'defense', ]

def getItem( level ):
    chooser = r.randint( 0, 2 )
    print( 'chooser : {}'.format(chooser))
    if chooser == 0:
        itemSlot = armorSlots[ int( r.random() * 4 ) ]
        value = 5 + 2 * level + int( ( r.random() - .5 ) * 6 )
        return items.armorObject.Armor( 'defaultRandomName', itemSlot, value )
    if chooser == 1:
        value = 5 + 2 * level + int( ( r.random() - .5 ) * 6 )
        return items.weaponObject.Weapon( 'defaultRandomName', value )
    if chooser == 2:
        attribute = consumableTypes[ int( r.random() * 3 ) ]
        duration = None
        if attribute == 'currentLife':
            value = 5 + 2 * level + int( ( r.random() -.5 ) * 4 )
        else :
            value = 3 + level + int( ( r.random() - .5 ) * 4 )
            duration = 3 + int( ( r.random() - .5 ) * 4 )
        return items.potionObject.Consumable( 'defaultRandomName', attribute, value, duration )
