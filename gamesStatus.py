import numpy as np


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

        # Engine variables
        n = 8
        self.moveLongNot = ''
        self.moveShortNot = ''
        self.validMoves = None
        self.validMovesFrom = np.array([0, 0])
        self.validMovesTo = np.array([0, -1])
        # Kings location for castling, check and mate
        self.kingLLoc = []
        self.kingDLoc = []
        # Separated valid moves
        self.validMovesFromDark = np.array([0, 0])
        self.validMovesToDark = np.array([0, -1])
        self.validMovesFromLight = np.array([0, 0])
        self.validMovesToLight = np.array([0, -1])

        self.testIteration = True

    def changeSide(self):
        if self.side == 'l':
            self.side = 'd'
        else:
            self.side = 'l'

    def clearStatus(self):
        self.newFig = ''

        # Engine variables
        n = 8
        self.moveLongNot = ''
        self.moveShortNot = ''
        self.validMoves = None
        self.validMovesFrom = np.array([0, 0])
        self.validMovesTo = np.array([0, -1])
        # Kings location for castling, check and mate
        self.kingLLoc = []
        self.kingDLoc = []
        # Separated valid moves
        self.validMovesFromDark = np.array([0, 0])
        self.validMovesToDark = np.array([0, -1])
        self.validMovesFromLight = np.array([0, 0])
        self.validMovesToLight = np.array([0, -1])

        self.testIteration = True

