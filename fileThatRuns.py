import mainGame
import tkinter as tk
import time
import sys

class GameView(tk.Frame):
    # gameState can be: normal, save, load
    gameState = 'normal'
    prevCommands = []
    prevSearchKey = 0

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Redirects all prints to the text field
        sys.stdout.write = self.printToView

        # Sets up the toolbar item
        self.toolbar = tk.Frame(self, bg='#eee')
        self.toolbar.pack(side = 'top', fill='x')

        # Sets up the label where the map will be, with
        # white text and a dark grey background
        self.map = tk.Label(self, text = '', font=('Consolas',14), bg = '#333', fg='#fff')
        self.map.pack(side = 'top', fill = 'x')

        # Sets up the entry field for commands
        self.textField = tk.Entry(self, font = ('Consolas',14))
        self.textField.pack(side = 'bottom', fill='x')
        self.textField.bind('<Key-Return>', self.entryField)
        self.textField.bind('<Key-Up>', self.lookForPrev)
        self.textField.bind('<Key-Down>', self.lookForPrev)

        # Sets up cache of previous commands
        self.commandHistory = tk.Text(self, font=('Consolas',8), bg='#eee', fg='#111', state="disabled")
        self.commandHistory.pack(side='top', fill='both')

        # Sets up the game itself
        self.game = mainGame.Game()

        # Places a save button in the toolbar that saves the game
        self.saveButton = tk.Button(self.toolbar, text='Save', command = self.saveGame, fg = '#000', bg = '#eee')
        self.saveButton.pack(side = 'left')

        # Places a load button in the toolbar that loads the game
        self.loadButton = tk.Button(self.toolbar, text='Load', command = self.loadGame, fg = '#000', bg = '#eee')
        self.loadButton.pack(side = 'left')

        # Places a quit button in the toolbar that ends the game
        self.quitButton = tk.Button(self.toolbar, text='Quit', command=self.quit, fg = '#000', bg = '#eee')
        self.quitButton.pack(side='right')

        # Sets up a changing map string
        self.textMap = tk.StringVar()
        self.textMap.set(self.game.drawMap())
        self.map.configure(textvariable=self.textMap)

    def entryField(self, Event):
        turnText = self.textField.get()
        print(turnText)
        if len(self.prevCommands)==0 or not(len(turnText)==0 or self.prevCommands[-1]==turnText):
            self.prevCommands+=[turnText]
        self.prevSearchKey = 0
        if self.gameState == 'normal':
            self.game.interpret(turnText)
            if self.game.textType == 'pass':
                print(' - passive command - ')
                self.game.passiveCommand()
            elif self.game.textType=='act':
                print(' - active command - ')
                self.game.activeCommand()

                # Checks for door collision
                if self.game.currentMap.mapCoordinateList[self.game.player.position[1]][self.game.player.position[0]]=="--":
                    for door in self.game.currentMap.connections:
                        if door[0][1] == tuple(self.game.player.position):
                            self.game.mapChange(door[1])
                            break

                # Updates all enemies
                self.mapCache = []
                self.mapCache = self.mapCache + [self.game.drawMap()]
                for actor in self.game.currentActors[1:]:
                    if actor.currentLife <= 0:
                        self.game.dungeonMaps[self.game.currentMap.name].enemyList.remove(actor)
                        self.game.currentActors.remove(actor)
                        self.game.dungeonMaps[self.game.currentMap.name].objectList += [actor.death()]
                    else:
                        actor.update(self.game.currentMap, self.game.currentActors+self.game.currentObjects, self.game.turnText)
                    print(actor.name)
                    self.mapCache = self.mapCache + [self.game.drawMap()]
                self.mapCache = self.mapCache + [self.game.drawMap()]
                self.after(0, self.toggleInteraction)
                self.after(0, self.drawFromCache)
            else:
                print('invalid command \'{}\', please type another valid command'.format(turnText))


        elif self.gameState == 'save':
            #code for save
            self.game.save(turnText)
            self.textMap.set(self.game.drawMap())
            self.gameState = 'normal'
        elif self.gameState == 'load':
            #code for load:
            self.game.load(turnText)
            self.textMap.set(self.game.drawMap())
            self.gameState = 'normal'
        self.textField.delete(0, 'end')

    def drawFromCache(self):
        self.textMap.set(self.mapCache.pop(0))
        if len(self.mapCache)>1:
            self.after(200,self.drawFromCache)
        else:
            self.toggleInteraction()

    # Possibly remove both
    def toggleInteraction(self):
        self.toggle_disable(self.textField)
        self.toggle_disable(self.saveButton)
        self.toggle_disable(self.loadButton)
        self.toggle_disable(self.quitButton)

    def toggle_disable(self, widgit):
        if widgit['state'] == 'normal':
            widgit.configure(state='disabled',fg='#555',bg='#aaa')
        elif widgit['state'] == 'disabled':
            widgit.configure(state='normal',fg='#000',bg='#eee')

    def saveGame(self):
        print('Please name your save...')
        self.gameState = 'save'

    def loadGame(self):
        self.game.loadSetup()
        self.gameState = 'load'

    # WORK ON THIS
    def quit(self):
        self.game.quit()

    def lookForPrev(self, Event):
        if Event.keycode==38:
            self.prevSearchKey = (self.prevSearchKey + 1) % (len(self.prevCommands))
            self.textField.delete(0,'end')
            self.textField.insert(0, self.prevCommands[-1*self.prevSearchKey])
        if Event.keycode==40:
            self.prevSearchKey = (self.prevSearchKey - 1) % (len(self.prevCommands))
            self.textField.delete(0,'end')
            self.textField.insert(0, self.prevCommands[-1*self.prevSearchKey])

    def printToView(self, printText):
        self.commandHistory.configure(state="normal")
        self.commandHistory.insert('end', printText)
        self.commandHistory.see('end')
        self.commandHistory.configure(state="disabled")

root = tk.Tk()
root.resizable(width = False, height = False)
root.geometry('{}x{}'.format(500,500))
GameView(root).pack(expand = 1, fill = 'both')
root.mainloop()