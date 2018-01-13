import tkinter as tk
import sys

class Userinter(tk.Frame):
    textList = ['It works!', 'It really does!']
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.toolbar = tk.Frame(self, bg='#eee')
        self.toolbar.pack(side='top', fill='x')

        self.red_btn = tk.Button(self.toolbar, text="Change", command = self.changeText)
        self.red_btn.pack(side="left")

        self.map = tk.Text(self)
        self.map.pack(side='bottom')

        sys.stdout.write = self.printToView

        print('Hello there!')

    def changeText(self):
        self.map.configure(textvariable = '\n'.join(self.textList))

    def printToView(self, printText):
        self.map.insert('end', printText)
        self.map.insert('end', "\n")
        self.map.see('end')
def demo():
    root = tk.Tk()
    Userinter(root).pack(expand=1, fill="both")
    root.textList = ['this appears to work too!']
    root.mainloop()


if __name__ == "__main__":
    demo()
