from chessEngine import ChessEngine
from gamesStatus import GameStatus
import numpy as np


class TextEngine:
    def __init__(self, boardSet, GS):
        self.boardSet = boardSet
        self.GS = GS
        self.prevPosRow = None
        self.prevPosCol = None
        self.newPosRow = None
        self.newPosCol = None
    
    def proceedData(self, text):
        data = list(bytes(text, 'ascii'))
        if 97 <= data[0] <= 104:
            self.prevPosCol = (data[0] - 97)
        else:
            return False

        if 49 <= data[1] <= 57:
            self.prevPosRow = 7 - (data[1] - 49)
        else:
            return False

        if 97 <= data[2] <= 104:
            self.newPosCol = (data[2] - 97)
        else:
            return False

        if 49 <= data[3] <= 57:
            self.newPosRow = 7 - (data[3] - 49)
        else:
            return False

        return True

    def isMoveValid(self):
        moved = False
        movesFrom = self.GS.validMovesFrom
        pieceLoc = np.array([self.prevPosRow, self.prevPosCol])
        i = 0
        fromIdx = []
        # Finding indexes of valid moves for our piece
        for loc in movesFrom:
            if loc[0] == pieceLoc[0] and loc[1] == pieceLoc[1]:
                fromIdx.append(i)
            i += 1
        # Generating all valid coordinates for piece move
        movesTo = self.GS.validMovesTo
        movesTo = np.take(movesTo, fromIdx, axis=0)
        
        where = None
        try:
            where = movesTo.tolist().index([self.newPosRow, self.newPosCol])
        except ValueError:
            where = None

        engine = ChessEngine(self.boardSet, self.GS)
        if where is not None:
            self.boardSet, self.GS = engine.move(self.prevPosRow, self.prevPosCol, movesTo[where][0], movesTo[where][1])
            # Game stack update
            self.GS.stackFrom.append([self.prevPosRow, self.prevPosCol])
            self.GS.stackTo.append([self.newPosRow, self.newPosCol])
            self.GS.changeSide()
            moved = True
        # Report check
        self.GS.clearStatus()
        self.GS = engine.checkCheck(self.boardSet, self.GS)
        return moved, self.boardSet, self.GS


