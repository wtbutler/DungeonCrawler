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
    currentActors = [player]
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
        ["attack",'act','attack a target enemy'],
        ['Lattack','act','attack a target enemy from anywhere','-TESTING ONLY-'],
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
            print(imageName)
            self.dungeonMaps[imageName[:-4]] = mapObject.DungeonMap(mapReading.getMapFromImage(self.path+"maps\\", imageName))
        self.dungeonMaps["Start"].setConnections(       [[["Start", (12,8)], ["dungeon2", (3,2)]],
                                                        [["Start",(18,3)],["dungeon1",(3,9)]]])
        self.dungeonMaps["dungeon1"].setConnections(    [[["dungeon1",(2,9)], ["Start",(17,3)]],
                                                        [["dungeon1",(8,14)],["dungeon2",(16,2)]]])
        self.dungeonMaps["dungeon2"].setConnections(    [[["dungeon2",(3,1)], ["Start",(12,7)]],
                                                        [["dungeon2",(16,1)],["dungeon1",(8,13)]]])

    ## DEBUG - REMOVE LATER - spawns enemies in rooms
    def debugSpace(self):
        self.dungeonMaps["Start"].actorList += [monsterObject.Monster("defaultName",[2,6], 1, items = ["Burning Sword", "Healing Potion"])]
        self.dungeonMaps["Start"].actorList += [monsterObject.Monster("defaultName2",[2,7], 1, items = ["Burning Sword", "Healing Potion"])]
        self.dungeonMaps["dungeon1"].actorList += [monsterObject.Monster("defaultName3",[5,6], 2)]
    # ^^^^^^^^^^^^^^^^^^

    # Changes enemies and map when the room changes
    def mapChange(self, destination):
        self.currentMap = self.dungeonMaps[destination[0]]
        self.currentActors = [self.player] + self.dungeonMaps[destination[0]].actorList
        self.currentObjects = self.dungeonMaps[destination[0]].objectList
        self.player.teleport(destination[1])
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
        for thing in self.currentActors+self.currentObjects:
            ## DEBUG - REMOVE LATER
            if self.debugMode == True:
                thing.updateInfo()
                print(thing.info)
            # ^^^^^^^^^^^^^^
            temporaryMap[thing.position[1]][thing.position[0]] = thing.icon
        tempList = []
        for i in temporaryMap:
            tempList += [''.join([str(x) for x in i])]
        return '\n'.join(tempList)

    # Def save/load functionality
    def save(self, saveName):
        if saveName != "":
            with open(self.path+"saves\\"+saveName+'.dat', 'wb') as f:
                pickle.dump([self.player, self.dungeonMaps, self.currentMap, self.currentActors, self.currentObjects], f)
        else:
            print("Please enter a name for your save file")

    def loadSetup(self):
        print('Please select save...')
        for saveName in os.listdir(self.path+"saves\\"):
            print(" "+saveName[:-4])

    def load(self, loadName):
        try:
            with open(self.path+"saves\\"+loadName+".dat", 'rb') as f:
                self.player, self.dungeonMaps, self.currentMap, self.currentActors, self.currentObjects = pickle.load(f)
                self.player.loadFromInfo()
            self.player.teleport(self.player.position)
            self.drawMap()
        except:
            print("invalid load file")

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
                    if self.turnText[1] == 'ntolaa':
                        self.debugMode = True
                        self.turnText.pop(1)
                    else:
                        self.textType = 'other'
                ## DEBUG - REMOVE LATER
                if self.debugMode == True:
                        print(self.textType+"ive command")
                # ^^^^^^^^^^^
                return
            self.textType = 'other'

    def do(self, actor, text):
        splitText = text.split(" ")

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
        if self.turnText[0] == "end":
            self.gameDone = True

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

    def activeCommand(self):
        # Code for active commands
        if self.textType == 'act':
            ## DEBUG - REMOVE LATER
            if self.debugMode == True:
                if self.turnText[0] == "Lattack":
                    try:
                        self.player.attack(self.currentActors[int(self.turnText[1])], self.currentActors)
                    except (ValueError, IndexError):
                        print("invalid enemy")
                        self.textType = 'pass'
                        return True
            # ^^^^^^^^^^^^^^^^^^^^^

            # Attack code
            if self.turnText[0] == "attack":
                try:
                    if self.player.findDistance(self.currentActors[int(self.turnText[1])].position)<4:
                        self.player.attack(self.currentActors[int(self.turnText[1])], self.currentActors)
                    else:
                        print("Too far away!")
                        self.textType = 'pass'
                        return True
                except (ValueError, IndexError):
                    print("invalid enemy")
                    self.textType = 'pass'
                    return True

            # Defines move commands
            if self.turnText[0] == 'move':
                try:
                    self.player.move(self.currentMap, self.currentActors+self.currentObjects, self.turnText[1])
                except:
                    print("Please input a valid dirction")
                    self.textType = 'pass'
                    return True
