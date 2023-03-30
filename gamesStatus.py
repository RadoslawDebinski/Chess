class GameStatus:
    def __init__(self):
        self.side = 'l'
        self.stackFrom = []
        self.stackTo = []
        # Is pawn available for enPassant
        self.isEnPassantL = [False] * 8
        self.isEnPassantD = [False] * 8
        # Is pawn available for promotion
        self.isPromotionL = [False] * 8
        self.isPromotionD = [False] * 8
        # Are king checked
        self.checkKingL = False
        self.checkKingD = False
        self.mateKingL = False
        self.mateKingD = False
        self.newFig = ''

    def changeSide(self):
        if self.side == 'l':
            self.side = 'd'
        else:
            self.side = 'l'


