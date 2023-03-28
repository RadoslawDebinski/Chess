class GameStatus:
    def __init__(self):
        self.side = 'l'

    def changeSide(self):
        if self.side == 'l':
            self.side = 'd'
        else:
            self.side = 'l'

