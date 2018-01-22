class Queue():
    actionList = []
    def __init__(self):
        self.actionList = []

    def emptyList(self):
        while (len(self.actionList)>0):
            print(self.actionList[0])
            self.actionList.pop(0)
        print("done")
