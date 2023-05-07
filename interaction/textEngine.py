from core.chessEngine import ChessEngine
from core.gamesStatus import GameStatus
import numpy as np
from itertools import zip_longest
import re


class TextEngine:
    def __init__(self, boardSet, GS):
        self.boardSet = boardSet
        n = 8
        self.squareSet = [list(t) for t in zip_longest(*[iter(self.boardSet)] * n, fillvalue=None)]
        self.GS = GS
        self.prevPosRow = None
        self.prevPosCol = None
        self.newPosRow = None
        self.newPosCol = None
        self.move = ''
    
    def applyMask(self):
        if 'x' in self.move:
            self.move = self.move.replace('x', '')
        if 'e.p.' in self.move:
            self.move = self.move.replace('e.p.', '')
        if '+' in self.move:
            self.move = self.move.replace('+', '')
        if '#' in self.move:
            self.move = self.move.replace('#', '')
        if '\n' in self.move:
            self.move = self.move.replace('\n', '')
        pattern = re.compile(r"^([RNBQK]?)([a-h]?)([1-8]?)([a-h][1-8])$")
        match = pattern.match(self.move)

        if match:
            return True
        else:
            return False

    def algebraicToLongNotation(self, move):
        self.move = move

        if not self.applyMask():
            return False

        if self.GS.side == 'd':
            pieces = {'K': 'k', 'Q': 'q', 'R': 'r', 'B': 'b', 'N': 'n'}
            validMovesFrom = self.GS.validMovesFromDark
            validMovesTo = self.GS.validMovesToDark

        else:
            pieces = {'K': 'K', 'Q': 'Q', 'R': 'R', 'B': 'B', 'N': 'N'}
            validMovesFrom = self.GS.validMovesFromLight
            validMovesTo = self.GS.validMovesToLight

        if self.move == '0-0':
            if self.GS.side == 'l':
                destinationRank = 7
                sourceRank = 7
            else:
                destinationRank = 0
                sourceRank = 0
            sourceFile = 4
            destinationFile = 6
        elif self.move == '0-0-0':
            if self.GS.side == 'l':
                destinationRank = 7
                sourceRank = 7
            else:
                destinationRank = 0
                sourceRank = 0
            sourceFile = 4
            destinationFile = 2
        else:
            # Determine the piece being moved
            if self.move[0] in pieces:
                piece = pieces[self.move[0]]
                startIndex = 1
            elif self.GS.side == 'l':
                piece = 'P'
                startIndex = 0
            else:
                piece = 'p'
                startIndex = 0

            ranks = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
            destinationRank = ranks[self.move[-1]]
            files = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

            destinationFile = files[self.move[-2]]
            # Finding indexes of valid moves
            toIdx = [i for i, loc in enumerate(validMovesTo) if loc[0] == destinationRank and loc[1] == destinationFile]
            fromPos = validMovesFrom[toIdx]
            validFrom = [i for i, loc in enumerate(fromPos) if self.squareSet[loc[0]][loc[1]] == piece]
            validFrom = fromPos[validFrom]

            if np.shape(validFrom)[0] == 0:
                return False
            if np.shape(validFrom)[0] > 1:
                if validFrom[0][0] == validFrom[1][0]:
                    try:
                        column = files[self.move[startIndex]]
                        validFrom = validFrom[np.any(np.where(validFrom == column, True, False), axis=1)][0]
                        sourceRank, sourceFile = validFrom
                    except KeyError:
                        return False

                elif validFrom[0][1] == validFrom[1][1]:
                    try:
                        row = files[self.move[startIndex]]
                        validFrom = validFrom[np.any(np.where(validFrom == row, True, False), axis=1)][0]
                        sourceRank, sourceFile = validFrom
                    except KeyError:
                        return False
                else:
                    try:
                        sourceRank, sourceFile = ranks[self.move[startIndex + 1]], files[self.move[startIndex]]
                    except KeyError:
                        return False
            else:
                validFrom = validFrom[0]
                sourceRank = validFrom[0]
                sourceFile = validFrom[1]

        self.prevPosRow = sourceRank
        self.prevPosCol = sourceFile
        self.newPosRow = destinationRank
        self.newPosCol = destinationFile
        return True

    def isMoveValid(self):
        moved = False
        movesFrom = self.GS.validMovesFrom
        pieceLoc = np.array([self.prevPosRow, self.prevPosCol])
        i = 0
        fromIdx = []
        # Finding indexes of valid moves for our piece
        fromIdx = [i for i, loc in enumerate(movesFrom) if loc[0] == pieceLoc[0] and loc[1] == pieceLoc[1]]

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


