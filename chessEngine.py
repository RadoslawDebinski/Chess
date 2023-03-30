import numpy as np


class ChessEngine:
    def __init__(self, boardSet, GS):
        self.boardSet = boardSet
        n = 8
        self.squareSet = [self.boardSet[i:i + n] for i in range(0, len(self.boardSet), n)]
        self.moveLongNot = ''
        self.moveShortNot = ''
        self.GS = GS
        self.side = self.GS.side
        self.validMoves = None
        self.validMovesFrom = np.array([0, 0])
        self.validMovesTo = np.array([0, 0])
        # Kings location for castling, check and mate
        self.kingLLoc = []
        self.kingDLoc = []
        # Separated valid moves
        self.validMovesFromDark = np.array([0, 0])
        self.validMovesToDark = np.array([0, 0])
        self.validMovesFromLight = np.array([0, 0])
        self.validMovesToLight = np.array([0, 0])

    def getValidMovesFrom(self):
        self.genValidMoves()
        return self.validMovesFrom

    def getValidMovesTo(self):
        self.genValidMoves()
        return self.validMovesTo

    def isValid(self, text, side):
        self.moveShortNot = text
        # here translation from short to long !!!
        self.moveLongNot = self.moveShortNot
        # here translation from long to indexes
        self.side = side
        self.genValidMoves()

    def genValidMoves(self):
        # calling functions for each piece on board and adding valid moves to list
        for r in range(len(self.squareSet)):
            for c in range(len(self.squareSet[r])):
                match self.squareSet[r][c].lower():
                    case 'r':
                        self.rook(r, c)
                    case 'n':
                        self.knight(r, c)
                    case 'b':
                        self.bishop(r, c)
                    case 'q':
                        self.queen(r, c)
                    case 'k':
                        if self.squareSet[r][c].islower():
                            self.kingDLoc = [r, c]
                        else:
                            self.kingLLoc = [r, c]
                        self.king(r, c)
                    case 'p':
                        self.pawn(r, c)
        # Separated list for dark and light
        self.separateMoves()
        # Short castling check
        self.shortCastling(self.kingLLoc[0], self.kingLLoc[1])
        self.shortCastling(self.kingDLoc[0], self.kingDLoc[1])
        # Long castling check
        self.longCastling(self.kingLLoc[0], self.kingLLoc[1])
        self.longCastling(self.kingDLoc[0], self.kingDLoc[1])
        return True

    def rook(self, r, c):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.squareSet[endRow][endCol]
                    if endPiece == ' ':  # empty space valid
                        self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                        self.validMovesTo = np.vstack((self.validMovesTo, [endRow, endCol]))
                    elif (endPiece.islower() and self.side == 'l' and self.squareSet[r][c].isupper()) or (
                            endPiece.isupper() and self.side != 'l' and self.squareSet[r][c].islower()):
                        # enemy piece is valid
                        self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                        self.validMovesTo = np.vstack((self.validMovesTo, [endRow, endCol]))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # out of board
                    break

    def knight(self, r, c):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                endPiece = self.squareSet[endRow][endCol]
                if endPiece == ' ':  # empty space valid
                    self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                    self.validMovesTo = np.vstack((self.validMovesTo, [endRow, endCol]))
                elif (endPiece.islower() and self.side == 'l' and self.squareSet[r][c].isupper()) or (
                        endPiece.isupper() and self.side != 'l' and self.squareSet[r][c].islower()):
                    # enemy piece is valid
                    self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                    self.validMovesTo = np.vstack((self.validMovesTo, [endRow, endCol]))

    def bishop(self, r, c):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.squareSet[endRow][endCol]
                    if endPiece == ' ':  # empty space valid
                        self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                        self.validMovesTo = np.vstack((self.validMovesTo, [endRow, endCol]))
                    elif (endPiece.islower() and self.side == 'l' and self.squareSet[r][c].isupper()) or (
                            endPiece.isupper() and self.side != 'l' and self.squareSet[r][c].islower()):
                        # enemy piece is valid
                        self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                        self.validMovesTo = np.vstack((self.validMovesTo, [endRow, endCol]))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # out of board
                    break

    def queen(self, r, c):
        self.rook(r, c)
        self.bishop(r, c)

    def king(self, r, c):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                endPiece = self.squareSet[endRow][endCol]
                if endPiece == ' ':  # empty space valid
                    self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                    self.validMovesTo = np.vstack((self.validMovesTo, [endRow, endCol]))
                elif (endPiece.islower() and self.side == 'l' and self.squareSet[r][c].isupper()) or (
                        endPiece.isupper() and self.side != 'l' and self.squareSet[r][c].islower()):
                    # enemy piece is valid
                    self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                    self.validMovesTo = np.vstack((self.validMovesTo, [endRow, endCol]))

    def pawn(self, r, c):
        if self.squareSet[r][c].isupper():  # light pawn moves
            if self.squareSet[r - 1][c] == ' ':
                self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                self.validMovesTo = np.vstack((self.validMovesTo, [r - 1, c]))
                if r == 6 and self.squareSet[r - 2][c] == ' ':
                    self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                    self.validMovesTo = np.vstack((self.validMovesTo, [r - 2, c]))
            if c - 1 >= 0:  # capture to the left
                if self.squareSet[r - 1][c - 1].islower() and self.squareSet[r][c].isupper():  # enemy piece to capture
                    self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                    self.validMovesTo = np.vstack((self.validMovesTo, [r - 1, c - 1]))
                # En passant 1.Free space 2.Move acceptable 3.Pawn nearby
                if self.squareSet[r - 1][c - 1] == ' ' and self.GS.isEnPassantD[c - 1] \
                        and self.squareSet[r][c - 1] == 'p':  # en passant to the left
                    self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                    self.validMovesTo = np.vstack((self.validMovesTo, [r - 1, c - 1]))
            if c + 1 <= 7:  # capture to the right
                if self.squareSet[r - 1][c + 1].islower() and self.squareSet[r][c].isupper():  # enemy piece to capture
                    self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                    self.validMovesTo = np.vstack((self.validMovesTo, [r - 1, c + 1]))
                # En passant 1.Free space 2.Move acceptable 3.Pawn nearby
                if self.squareSet[r - 1][c + 1] == ' ' and self.GS.isEnPassantD[c + 1] \
                        and self.squareSet[r][c + 1] == 'p':  # en passant to the right
                    self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                    self.validMovesTo = np.vstack((self.validMovesTo, [r - 1, c + 1]))

        else:  # dark pawn moves
            if self.squareSet[r + 1][c] == ' ':
                self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                self.validMovesTo = np.vstack((self.validMovesTo, [r + 1, c]))
                if r == 1 and self.squareSet[r + 2][c] == ' ':
                    self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                    self.validMovesTo = np.vstack((self.validMovesTo, [r + 2, c]))
            if c - 1 >= 0:  # capture to the left
                if self.squareSet[r + 1][c - 1].isupper() and self.squareSet[r][c].islower():  # enemy piece to capture
                    self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                    self.validMovesTo = np.vstack((self.validMovesTo, [r + 1, c - 1]))
                # En passant 1.Free space 2.Move acceptable 3.Pawn nearby
                if self.squareSet[r + 1][c - 1] == ' ' and self.GS.isEnPassantL[c - 1] \
                        and self.squareSet[r][c - 1] == 'P':  # en passant to the left
                    self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                    self.validMovesTo = np.vstack((self.validMovesTo, [r + 1, c - 1]))
            if c + 1 <= 7:  # capture to the right
                if self.squareSet[r + 1][c + 1].isupper() and self.squareSet[r][c].islower():  # enemy piece to capture
                    self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                    self.validMovesTo = np.vstack((self.validMovesTo, [r + 1, c + 1]))
                # En passant 1.Free space 2.Move acceptable 3.Pawn nearby
                if self.squareSet[r + 1][c + 1] == ' ' and self.GS.isEnPassantL[c + 1] \
                        and self.squareSet[r][c - 1] == 'P':  # en passant to the right
                    self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                    self.validMovesTo = np.vstack((self.validMovesTo, [r + 1, c + 1]))

    def separateMoves(self):
        for i, j in zip(self.validMovesFrom, self.validMovesTo):
            if self.squareSet[i[0]][i[1]].islower():
                self.validMovesFromDark = np.vstack((self.validMovesFromDark, i))
                self.validMovesToDark = np.vstack((self.validMovesToDark, j))
            elif self.squareSet[i[0]][i[1]].isupper():
                self.validMovesFromLight = np.vstack((self.validMovesFromLight, i))
                self.validMovesToLight = np.vstack((self.validMovesToLight, j))

    def shortCastling(self, r, c):
        kingNotAvailable = []
        try:
            kingNotAvailable = self.GS.stackFrom.index([r, c])
        except ValueError:
            kingNotAvailable = []
        if not kingNotAvailable:
            rookNotAvailable = []
            try:
                rookNotAvailable = self.GS.stackFrom.index([r, c + 3])
                print("hi")
            except ValueError:
                rookNotAvailable = []
                if not rookNotAvailable:
                    path = [self.squareSet[r][c + 1], self.squareSet[r][c + 2]]
                    clearPath = all(ele == ' ' for ele in path)
                    if clearPath:
                        if self.shortCastlingPathSafety(r, c):
                            self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                            self.validMovesTo = np.vstack((self.validMovesTo, [r, c + 2]))

    def shortCastlingPathSafety(self, r, c):
        fColCords = [r, c + 1]
        gColCords = [r, c + 2]

        if self.side == 'l':
            fSafe = np.any(np.all(np.where(fColCords == self.validMovesToDark, True, False), axis=1))
            gSafe = np.any(np.all(np.where(gColCords == self.validMovesToDark, True, False), axis=1))
            if fSafe or gSafe:
                return False
        else:
            fSafe = np.any(np.all(np.where(fColCords == self.validMovesToLight, True, False), axis=1))
            gSafe = np.any(np.all(np.where(gColCords == self.validMovesToLight, True, False), axis=1))
            if fSafe or gSafe:
                return False
        return True

    def longCastling(self, r, c):
        kingNotAvailable = []
        try:
            kingNotAvailable = self.GS.stackFrom.index([r, c])
        except ValueError:
            kingNotAvailable = []
        if not kingNotAvailable:
            rookNotAvailable = []
            try:
                rookNotAvailable = self.GS.stackFrom.index([r, c - 4])
            except ValueError:
                rookNotAvailable = []
                if not rookNotAvailable:
                    path = [self.squareSet[r][c - 1], self.squareSet[r][c - 2], self.squareSet[r][c - 3]]
                    clearPath = all(ele == ' ' for ele in path)
                    if clearPath:
                        if self.longCastlingPathSafety(r, c):
                            self.validMovesFrom = np.vstack((self.validMovesFrom, [r, c]))
                            self.validMovesTo = np.vstack((self.validMovesTo, [r, c - 2]))

    def longCastlingPathSafety(self, r, c):
        cColCords = [r, c - 1]
        dColCords = [r, c - 2]

        if self.side == 'l':
            fSafe = np.any(np.all(np.where(cColCords == self.validMovesToDark, True, False), axis=1))
            gSafe = np.any(np.all(np.where(dColCords == self.validMovesToDark, True, False), axis=1))
            if fSafe or gSafe:
                return False
        else:
            fSafe = np.any(np.all(np.where(cColCords == self.validMovesToLight, True, False), axis=1))
            gSafe = np.any(np.all(np.where(dColCords == self.validMovesToLight, True, False), axis=1))
            if fSafe or gSafe:
                return False
        return True

    def enPassantReport(self, startRow, startCol, endRow, endCol):
        # En passant availability for light
        if self.squareSet[startRow][startCol] == 'P':
            if startRow == 6 and endRow == 4:
                self.GS.isEnPassantL[endCol] = True
        # En passant availability for dark
        if self.squareSet[startRow][startCol] == 'p':
            if startRow == 1 and endRow == 3:
                self.GS.isEnPassantD[endCol] = True
        # En passant dark reset
        if self.GS.side == 'l':
            self.GS.isEnPassantD = [False] * 8
        # En passant light reset
        else:
            self.GS.isEnPassantL = [False] * 8

    def move(self, startRow, startCol, endRow, endCol):
        # Report en passant availability or reset it
        self.enPassantReport(startRow, startCol, endRow, endCol)

        # Change figures coordinates start <-> end [temporary]
        temp = self.squareSet[endRow][endCol]
        self.squareSet[endRow][endCol] = self.squareSet[startRow][startCol]
        self.squareSet[startRow][startCol] = temp

        # Game stack update
        self.GS.stackFrom.append([startRow, startCol])
        self.GS.stackTo.append([endRow, endCol])

        # Next Player
        self.GS.changeSide()

        return list(np.array(self.squareSet).flatten())
