class Tile:
    def __init__(self):
        self.number = None
        self.posNums = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    def __str__(self):
        #Used for debugging
        if len(self.posNums)>0:
            return repr(self.posNums)
        return str(self.number)