class GameStatus:
    def __init__(self):
        self.side = 'l'
        self.stackFrom = []
        self.stackTo = []
        # Is pawn available for enPassant
        self.isEnPassantL = [False] * 8
        self.isEnPassantD = [False] * 8
        # Are king checked
        self.checkKingL = False
        self.checkKingD = False

    def changeSide(self):
        if self.side == 'l':
            self.side = 'd'
        else:
            self.side = 'l'


