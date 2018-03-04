import mainGame
import tkinter as tk
import time
import sys
import util

class GameView(tk.Frame):
    # gameState can be: normal, save, load
    prevCommands = []
    prevSearchKey = 0
    mapCache = []

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Redirects all prints to the text field
        sys.stdout.write = self.myPrint
        self.utils = util.TextControl()

        self.mapCache = []

        # Sets the window name
        self.winfo_toplevel().title("Dungeon Crawler")

        # Sets up the toolbar item
        self.toolbar = tk.Frame(self, bg='#eee')
        self.toolbar.pack(side = 'top', fill='x')

        # Sets up the label where the map will be, with
        # white text and a dark grey background
        self.map = tk.Label(self, text = '', font=('Consolas',14), bg = '#333', fg='#fff')
        self.map.pack(side = 'left', fill = 'y')

        # Sets up the entry field for commands
        self.textField = tk.Entry(self, font = ('Consolas',14))
        self.textField.pack(side = 'bottom', fill='x')
        self.textField.bind('<Key-Return>', self.entryField)
        self.textField.bind('<Key-Up>', self.lookForPrev)
        self.textField.bind('<Key-Down>', self.lookForPrev)
        self.textField.focus_set()

        # Sets up cache of previous commands
        self.commandHistory = tk.Text(self, font=('Consolas',8), bg='#eee', fg='#111', state="disabled")
        self.commandHistory.pack(side='bottom', fill='both', expand=1)

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
        if len(self.prevCommands)==0 or not(len(turnText)==0 or self.prevCommands[-1]==turnText):
            self.prevCommands+=[turnText]
        self.prevSearchKey = 0
        if self.utils.gameState == 'normal':
            print('turnText: {}'.format(turnText))
            self.utils.gameState = self.game.interpret(turnText)

            if self.game.textType == 'pass':
                print(' - passive command - ')
                self.game.passiveCommand()

            elif self.game.textType=='act':
                print(' - active command - ')
                self.game.activeCommand()
                if self.game.textType=='act': self.game.updateOtherActors()
            else:
                print('invalid command \'{}\', please type another valid command'.format(turnText))

            self.after(0, self.toggleInteraction)
            self.utils.addMap(self.game.drawMap())
            self.after(200, self.drawFromCache)

        elif self.utils.gameState == 'save':
            #code for save
            self.game.save(turnText)
            self.textMap.set(self.game.drawMap())
            self.utils.gameState = 'normal'
        elif self.utils.gameState == 'load':
            #code for load:
            self.game.load(turnText)
            self.textMap.set(self.game.drawMap())
            self.utils.gameState = 'normal'
        elif self.utils.gameState == 'quit':
            # code for quitting
            # if turnText=='yes' or turnText=='y':
                global root
                root.quit()
        self.textField.delete(0, 'end')

    def drawFromCache(self):
        self.textMap.set(self.utils.mapCache.pop(0))
        if len(self.utils.mapCache)>=1:
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
        self.utils.gameState = 'save'

    def loadGame(self):
        self.game.loadSetup()
        self.utils.gameState = 'load'

    def quit(self):
        print('Are you sure you want to quit? [Y/N]')
        self.utils.gameState = 'quit'

    def lookForPrev(self, Event):
        if Event.keycode==38:
            self.prevSearchKey = (self.prevSearchKey + 1) % (len(self.prevCommands))
            self.textField.delete(0,'end')
            self.textField.insert(0, self.prevCommands[-1*self.prevSearchKey])
        if Event.keycode==40:
            self.prevSearchKey = (self.prevSearchKey - 1) % (len(self.prevCommands))
            self.textField.delete(0,'end')
            self.textField.insert(0, self.prevCommands[-1*self.prevSearchKey])

    def myPrint(self, text):
        self.printToView(text)

    def printToView(self, printText):
        self.commandHistory.configure(state="normal")
        self.commandHistory.insert('end', printText)
        self.commandHistory.see('end')
        self.commandHistory.configure(state="disabled")

root = tk.Tk()
root.resizable(width = False, height = False)
root.geometry('{}x{}+{}+{}'.format(1000,500,50,50))
GameView(root).pack(expand = 1, fill = 'both')
root.mainloop()
