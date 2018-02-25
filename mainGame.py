import os, sys
import mapReading
import playerCharacter
import mapObject
import monsterObject
import pickle
import chestObject

class Game():
    player = playerCharacter.PlayerCharacter(2,2)
    currentMap = 0
    currentActors = []
    currentObjects = []
    textType = "other"
    prevText = ""
    turnTextRaw = ""
    turnText = ""
    gameDone = False
    debugMode = False
    path = ""
    dungeonMaps = {}
    keywords = [
        ["move",'act','move around the map'],
        ['right',0,'direction to move'],
        ['left',0,'direction to move'],
        ['up',0,'direction to move'],
        ['down',0,'direction to move'],
        ["attack",'act','attack in a direction'],
        ['broad', 5,'attack 3 squares weakly in a direction'],
        ["info",'pass','displays position about a target','-TESTING ONLY-'],
        ["mapinfo",'pass','displays information about the map','-TESTING ONLY-'],
        ["test",'pass','run a command of python script','-TESTING ONLY-'],
        ["items",'pass','print the currently held items'],
        ["help",'pass','print a list of commands'],
        ["save",'pass','save the current game'],
        ["load",'pass','load a previous game'],
        ["end",'pass','ends the current game']
        ]

    # Initializes the game object
    def __init__(self):
        self.findPath()
        self.loadMaps()
        self.debugSpace()
        self.mapChange(("Start", (2,2)))

    # Locates dungeon maps
    def findPath(self):
        self.path = os.path.dirname(os.path.realpath(__file__))+"\\"

    # Initializes objects for maps
    def loadMaps(self):
        self.dungeonMaps = {}
        for imageName in os.listdir(self.path+"maps\\"):
            self.dungeonMaps[imageName[:-4]] = mapObject.DungeonMap(mapReading.getMapFromImage(self.path+"maps\\", imageName))
        self.dungeonMaps["Start"].setConnection(       [["Start", (8,12)]  ,   ["dungeon2", (2,3)]])
        self.dungeonMaps["Start"].setConnection(       [["Start",(3,18)]   ,   ["dungeon1",(9,3)]] )
        self.dungeonMaps["dungeon1"].setConnection(    [["dungeon1",(9,2)] ,   ["Start",(3,17)]]   )
        self.dungeonMaps["dungeon1"].setConnection(    [["dungeon1",(14,8)],   ["dungeon2",(2,16)]])
        self.dungeonMaps["dungeon2"].setConnection(    [["dungeon2",(1,3)] ,   ["Start",(7,12)]]   )
        self.dungeonMaps["dungeon2"].setConnection(    [["dungeon2",(1,16)],   ["dungeon1",(13,8)]])

    ## DEBUG - REMOVE LATER - spawns enemies in rooms
    def debugSpace(self):
        self.dungeonMaps["Start"].addCreature(monsterObject.Monster("defaultName",[6,2], 1, items = ["Burning Sword", "Healing Potion"]))
        self.dungeonMaps["Start"].addCreature(monsterObject.Monster("defaultName2",[7,2], 1, items = ["Burning Sword", "Healing Potion"]))
        self.dungeonMaps["dungeon1"].addCreature(monsterObject.Monster("defaultName3",[6,5], 2))
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

    # Def save functionality
    def save(self, saveName):
        if saveName != "":
            with open(self.path+"saves\\"+saveName+'.dat', 'wb') as f:
                pickle.dump([self.player, self.dungeonMaps, self.currentMap, self.currentActors, self.currentObjects], f)
        else:
            print("Please enter a name for your save file")

    # Shows all saved files for selection to load
    def loadSetup(self):
        print('Please select save...')
        for saveName in os.listdir(self.path+"saves\\"):
            if saveName!='emp.ty':
                print(" "+saveName[:-4])

    # loads the file chosen
    def load(self, loadName):
        try:
            with open(self.path+"saves\\"+loadName+".dat", 'rb') as f:
                self.player, self.dungeonMaps, self.currentMap, self.currentActors, self.currentObjects = pickle.load(f)
                # self.player.loadFromInfo()
            self.player.teleport(self.player.position)
            self.drawMap()
            print("Successfully loaded from {}".format(loadName))
        except:
            print("invalid load file")

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
        print('toMap')
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

    # Performs the different passive commands player
    def passiveCommand(self):
        # Code for passive commands
        ## DEBUG information and commands - REMOVE LATER
        if self.debugMode == True:
            if self.turnText[0] == "mapinfo":
                print(self.currentMap.mapInfo)

            if self.turnText[0] == "info":
                try:
                    print(self.currentActors[int(self.turnText[1])].info)
                except (ValueError, IndexError):
                    print("Invalid selection")
                    self.drawInfo()

            if self.turnText[0] == "position":
                print(self.player.position)

        if self.turnText[0] == "test":
            if self.debugMode == True:
                try:
                    print('-----\n')
                    exec(" ".join(self.turnText[1:]))
                    print('\nexecuted')
                except Exception as e:
                    print('you typed it wrong:\n{}'.format(e))
                    return True
            else:
                print("Unknown command 'test', please try again")
                return True

        # ^^^^^^^^^^^^^^^^^^^^^

        # Regular Commands
        if self.turnText[0] == "items":
            print(self.player.items)

        if self.turnText[0] == "help":
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
        if self.gameDone == True:
            return False
        return True

    # Performs the different active commands player
    def activeCommand(self):
        decision = self.player.update(self.turnText)

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
        print('toMap')

    def updateOtherActors(self):
        for actor in self.currentActors:
            decision = ''
            if actor.currentLife <= 0:
                self.currentMap.tileAt(actor.position).emptyThis()
                self.currentActors.remove(actor)
                self.currentMap.addObject(actor.death())
                print('currentMapActors after Death: {}'.format(self.currentMap.actorList))
            else:
                decision = actor.update(self.testWalls(actor.position), self.player.position)
                if decision[0]=='move':
                    self.move(actor, decision[1])
                if decision[0]=='attack':
                    self.attack(decision[1], decision[2])
            print('toMap')
