import os, sys
import pickle

import util

import maps.mapReading
import maps.mapObject

import actors.playerCharacter
import actors.monsterObject
import actors.chestObject

import items.potionObject
import items.armorObject
import items.weaponObject

class Game():
    player = 0
    currentMap = 0
    currentActors = []
    textType = "other"
    turnText = ""
    debugMode = False
    path = ""
    dungeonMaps = {}
    utils = ''
    keywords = [
        ["move",'act','Move around the map \'move <direction>\''],
        ['right',0,'Direction to move \'right\''],
        ['left',0,'Direction to move \'left\''],
        ['up',0,'Direction to move \'up\''],
        ['down',0,'Direction to move \'down\''],
        ["attack",'act','Attack in a direction \'attack <type> <direction>\''],
        ['broad', 5,'Attack 3 squares weakly in a direction \'broad <direction>\''],
        ['wait', 'act', 'Wait in place while other creatures move'],
        ['check', 'pass', 'Give information about a given direction \'check <direction>\''],
        ['take', 'pass', 'Loot or destroy a chest \'take <direction> <item #>\''],
        ['inv', 'pass', 'Shows your inventory \'inv\''],
        ['use', 'pass', 'Use or equip an item from your inventory \'use <item #>\''],
        ['drop', 'pass', 'Removes an item from your inventory forever \'drop <item #>\''],
        ["test",'pass','Run a command of python script','-TESTING ONLY-'],
        ["help",'pass','Print a list of commands'],
        ["save",'pass','Save the current game'],
        ["load",'pass','Load a previous game'],
        ["end",'pass','Ends the current game']
        ]

    # Initializes the game object
    def __init__(self):
        self.player = actors.playerCharacter.PlayerCharacter(2,2)
        self.findPath()
        self.loadMaps()
        self.debugSpace()
        self.mapChange(("Start", (2,2)))
        self.utils = util.TextControl()

    # Locates dungeon maps
    def findPath(self):
        self.path = os.path.dirname(os.path.realpath(__file__))+"/"

    # Initializes objects for maps
    def loadMaps(self):
        self.dungeonMaps = {}
        for imageName in os.listdir(self.path+"maps/mapimages/"):
            self.dungeonMaps[imageName[:-4]] = maps.mapObject.DungeonMap(maps.mapReading.getMapFromImage(self.path+"maps/mapimages/", imageName))
        self.dungeonMaps["Start"].setConnection(       [["Start", (8,12)]  ,   ["dungeon2", (2,3)]])
        self.dungeonMaps["Start"].setConnection(       [["Start",(3,18)]   ,   ["dungeon1",(9,3)]] )
        self.dungeonMaps["dungeon1"].setConnection(    [["dungeon1",(9,2)] ,   ["Start",(3,17)]]   )
        self.dungeonMaps["dungeon1"].setConnection(    [["dungeon1",(14,8)],   ["dungeon2",(2,16)]])
        self.dungeonMaps["dungeon2"].setConnection(    [["dungeon2",(1,3)] ,   ["Start",(7,12)]]   )
        self.dungeonMaps["dungeon2"].setConnection(    [["dungeon2",(1,16)],   ["dungeon1",(13,8)]])

    ## DEBUG - REMOVE LATER - spawns enemies in rooms
    def debugSpace(self):
        self.dungeonMaps["Start"].addCreature(actors.monsterObject.Monster("defaultName",[6,2], 1, itemCount = 2))
        self.dungeonMaps["Start"].addCreature(actors.monsterObject.Monster("defaultName2",[7,2], 1, itemCount = 2))
        self.dungeonMaps["dungeon1"].addCreature(actors.monsterObject.Monster("defaultName3",[6,5], 2))
        return
    # ^^^^^^^^^^^^^^^^^^

    # Changes enemies and map when the room changes
    def mapChange(self, destination):
        target = [destination[1][0],destination[1][1]]
        self.currentMap = self.dungeonMaps[destination[0]]
        self.currentActors = self.dungeonMaps[destination[0]].actorList
        self.currentObjects = self.dungeonMaps[destination[0]].objectList
        self.player.position=target
        self.currentMap.tileAt(target).actor=self.player
        self.drawMap()

    # Draws info about enemies
    def drawInfo(self):
        if len(self.currentActors)>1:
            print("Enemies:")
            for i in range(1,len(self.currentActors)):
                print("  {}: {}".format(i, self.currentActors[i].name))
        else:
            print("No enemies")

    # Returns the visual map
    def drawMap(self):
        temporaryMap = []
        # Adds each row by piece, as a copy of the mapCoordinateList
        for row in self.currentMap.mapCoordinateList:
            temporaryMap += [row[:]]
        # for thing in self.currentActors+self.currentObjects:
        #     ## DEBUG - REMOVE LATER
        #     if self.debugMode == True:
        #         thing.updateInfo()
        #         print(thing.info)
        #     # ^^^^^^^^^^^^^^
        #     temporaryMap[thing.position[1]][thing.position[0]] = thing.icon
        tempList = []
        for i in temporaryMap:
            tempList += [''.join([str(x) for x in i])]
        return '\n'.join(tempList)

    # Returns walls for non-player stuff [up, right, down, left]
    def testWalls(self, position):
        testables = [self.currentMap.tileAt([position[0]-1, position[1]]),
                     self.currentMap.tileAt([position[0], position[1]+1]),
                     self.currentMap.tileAt([position[0]+1, position[1]]),
                     self.currentMap.tileAt([position[0], position[1]-1])]
        toReturn = [False, False, False, False]
        for i in range(len(testables)):
            if testables[i].canPlace(): toReturn[i] = True
        return toReturn

    # moves an actor object from their current position to a coordinate on the current map
    def move(self, actor, targetCoords):
        if actor.position==targetCoords: return
        target=self.currentMap.tileAt(targetCoords)
        position=self.currentMap.tileAt(actor.position)
        # Target and Position are both tile objects from the relevent positions
        if target.isEmpty():
            position.emptyThis()
            actor.position=targetCoords
            if target.tileType()=='floor':
                target.actor=actor
            elif target.tileType()=='door':
                self.mapChange(target.getConnection())
            else:
                print('\nALERT\n\nTHERE HAS BEEN A MAJOR ERROR\n\nALERT\n')
        else:
            print("That square cannot be moved into")

    # attacks a list of coordinates with a set amount of damage
    def attack(self, damage, tileList):
        # give tiles as coordinates, not as tile objects
        for tile in tileList:
            if self.currentMap.tileAt(tile).tileType()=='floor':
                self.currentMap.tileAt(tile).attack(damage)
        self.utils.addMap(self.drawMap())
        for tile in tileList:
            if self.currentMap.tileAt(tile).tileType()=='floor':
                self.currentMap.tileAt(tile).default()

    # Takes the input text and matches it to one of the members of the command list
    def interpret(self, rawText):
        self.turnText = rawText.split(" ")

        # Interprets the command
        for key in self.keywords:
            if self.turnText[0] == key[0]:
                if key[1]=='pass' or key[1] =='act':
                    self.textType = key[1]
                else:
                    self.turnText.insert(0,self.keywords[key[1]][0])
                    self.textType = self.keywords[key[1]][1]
                if (self.debugMode == False) and len(key) > 3:
                    if len(self.turnText)>1 and self.turnText[1] == 'ntolaa':
                        self.debugMode = True
                        self.turnText.pop(1)
                    else:
                        self.textType = 'other'
                ## DEBUG - REMOVE LATER
                if self.debugMode == True:
                        print(self.textType+"ive command")
                # ^^^^^^^^^^^
                if self.turnText[0] == 'end':
                    print('Are you sure you want to quit? [Y/N]')
                    return 'quit'
                if self.turnText[0] == 'save':
                    print('Please name your save...')
                    return 'save'
                if self.turnText[0] == 'load':
                    self.loadSetup()
                    return 'load'
                return 'normal'
        self.textType = 'other'
        return 'normal'

    # Prints info about something in a direction
    def check(self, direction):
        position = self.player.position
        target = []
        if direction=='left': target = [position[0],position[1]-1]
        if direction=='down': target = [position[0]+1,position[1]]
        if direction=='right': target = [position[0],position[1]+1]
        if direction=='up': target = [position[0]-1,position[1]]
        if direction=='me': target = position
        if target!=[]:
            self.currentMap.tileAt(target).check()
            return
        print('Please give a valid direction')

    def takeItem(self, direction):
        position = self.player.position
        target = []
        if direction=='left': target = [position[0],position[1]-1]
        if direction=='down': target = [position[0]+1,position[1]]
        if direction=='right': target = [position[0],position[1]+1]
        if direction=='up': target = [position[0]-1,position[1]]
        if target==[]:
            print('Please give a valid direction')
            return
        chest = self.currentMap.tileAt(target).actor
        if not(type(chest) is actors.chestObject.Chest):
            print('There is not a chest there!')
            return
        try:
            # Takes all items from chest and then destroys it
            if self.turnText[2]=='all':
                while len(chest.items)>=0:
                    item = chest.take(1, takeAll=True)
                    if item=='breakThis':
                        self.currentMap.tileAt(target).emptyThis()
                        print('You destroyed the empty chest.')
                        return
                    self.player.addItem(item)

            item = chest.take(int(self.turnText[2]))
            if item==None: raise IndexError('Invalid item from chest')
            if item=='breakThis':
                self.currentMap.tileAt(target).emptyThis()
                print('You destroyed the empty chest.')
                return
            self.player.addItem(item)
        except (IndexError, ValueError) as e:
            print('Please enter a valid item number, {}'.format(repr(e)))
            return


    # Prints a list of all commands available to the player
    def help(self):
        for command in self.keywords:
            if self.debugMode == False:
                if len(command) == 3:
                    if command[1] == 'pass' or command[1]=='act':
                        print(" - "+command[0] + ' : '+" ".join(command[2:]))
                    else:
                        print(" -   "+command[0]+ ' : ' + " ".join(command[2:]))
            else:
                if command[1] == 'pass' or command[1]=='act':
                    print(" - "+command[0] + ' : '+" ".join(command[2:]))
                else:
                    print(" -   "+command[0]+ ' : ' + " ".join(command[2:]))

    # Def save functionality
    def save(self, saveName):
        if saveName != "":
            with open(self.path+"saves/"+saveName+'.dat', 'wb') as f:
                pickle.dump([self.player, self.dungeonMaps, self.currentMap, self.currentActors, self.currentObjects], f)
        else:
            print("Please enter a name for your save file")

    # Shows all saved files for selection to load
    def loadSetup(self):
        print('Please select save...')
        for saveName in os.listdir(self.path+"saves/"):
            if saveName!='emp.ty':
                print(" "+saveName[:-4])

    # loads the file chosen
    def load(self, loadName):
        try:
            with open(self.path+"saves/"+loadName+".dat", 'rb') as f:
                self.player, self.dungeonMaps, self.currentMap, self.currentActors, self.currentObjects = pickle.load(f)
            self.player.teleport(self.player.position)
            self.drawMap()
            print("Successfully loaded from {}".format(loadName))
        except:
            print("invalid load file")

    # Performs the different passive commands player
    def passiveCommand(self):
        ## DEBUG information and commands - REMOVE LATER
        if self.turnText[0] == "test":
            if self.debugMode == True:
                try:
                    print('-----\n')
                    exec(" ".join(self.turnText[1:]))
                    print('\nexecuted')
                except Exception as e:
                    print('you typed it wrong:\n{}'.format(e))
            else:
                print("Unknown command 'test', please try again")
        # ^^^^^^^^^^^^^^^^^^^^^

        # Regular Commands
        if self.turnText[0] == "check":
            if len(self.turnText)>1: self.check(self.turnText[1])
            else: print('Please enter a direction')

        if self.turnText[0] == "take":
            if len(self.turnText)>1: self.takeItem(self.turnText[1])
            else: print('Please enter a direction')

        if self.turnText[0] == "help":
            self.help()

        if self.turnText[0] == 'inv':
            for i in range(len(self.player.itemList)):
                print(' - {} {}'.format(i+1, repr(self.player.itemList[i])))

        if self.turnText[0] == 'use':
            try:
                itemIndex = int(self.turnText[1])
            except ValueError as e:
                print('Please enter a valid number')
                return
            print('itemIndex: {}'.format(itemIndex))
            self.player.useItem(itemIndex)

        if self.turnText[0] == 'drop':
            try:
                itemIndex = int(self.turnText[1])
            except ValueError as e:
                print('Please enter a valid number')
                return
            print('itemIndex: {}'.format(itemIndex))
            self.player.dropItem(itemIndex)

    # Performs the different active commands player
    def activeCommand(self):
        decision = self.player.update(self.turnText)
        if decision=='break':
            self.textType = 'pass'
            return

        # Attack code
        if decision[0]=='attack':
            try:
                self.attack(decision[1], decision[2])
            except Exception as e:
                print("Please input a valid dirction", e)
                self.textType = 'pass'

        # Defines move commands
        if decision[0] == 'move':
            try:
                self.move(self.player, decision[1])
            except Exception as e:
                print("Please input a valid dirction", e)
                self.textType = 'pass'

        if decision[0]=='wait': pass


        self.utils.addMap(self.drawMap())

    # Performs all actions for other actors
    def updateOtherActors(self):
        toDel=[]
        for actor in self.currentActors:
            decision = ''
            if actor.currentLife <= 0:
                self.currentMap.tileAt(actor.position).emptyThis()
                toDel+=[actor]
                self.currentMap.addObject(actor.death())
            else:
                decision = actor.update(self.testWalls(actor.position), self.player.position)
                if decision[0]=='move':
                    self.move(actor, decision[1])
                if decision[0]=='attack':
                    self.attack(decision[1], decision[2])
            self.utils.addMap(self.drawMap())
        for actor in toDel:
            self.currentActors.remove(actor)
