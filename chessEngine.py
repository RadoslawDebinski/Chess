import numpy as np
import copy


class ChessEngine:
    def __init__(self, boardSet, GS):
        self.boardSet = boardSet
        self.GS = GS
        n = 8
        self.squareSet = [self.boardSet[i:i + n] for i in range(0, len(self.boardSet), n)]

    def isValid(self, text, side):
        self.GS.moveShortNot = text
        # here translation from short to long !!!
        self.GS.moveLongNot = self.GS.moveShortNot
        # here translation from long to indexes
        self.GS.side = side
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
                            self.GS.kingDLoc = [r, c]
                        else:
                            self.GS.kingLLoc = [r, c]
                        self.king(r, c)
                    case 'p':
                        self.pawn(r, c)
        # Separated list for dark and light to check castling
        self.separateMoves()
        # Short castling check
        self.shortCastling(self.GS.kingLLoc[0], self.GS.kingLLoc[1])
        self.shortCastling(self.GS.kingDLoc[0], self.GS.kingDLoc[1])
        # Long castling check
        self.longCastling(self.GS.kingLLoc[0], self.GS.kingLLoc[1])
        self.longCastling(self.GS.kingDLoc[0], self.GS.kingDLoc[1])
        return True

    #############################################
    # self.GS.side == 'l' <----> startPiece.isupper()
    # self.GS.side != 'l' <----> startPiece.islower()
    #############################################
    def rook(self, r, c):
        startPiece = self.squareSet[r][c]
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.squareSet[endRow][endCol]
                    if endPiece == ' ':  # empty space valid
                        if self.checkFutureBoi(r, c, endRow, endCol):
                            self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                            self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [endRow, endCol]))
                    elif (endPiece.islower() and startPiece.isupper() and self.squareSet[r][c].isupper()) or (
                            endPiece.isupper() and startPiece.islower() and self.squareSet[r][c].islower()):
                        # enemy piece is valid
                        if self.checkFutureBoi(r, c, endRow, endCol):
                            self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                            self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [endRow, endCol]))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # out of board
                    break

    def knight(self, r, c):
        startPiece = self.squareSet[r][c]
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                endPiece = self.squareSet[endRow][endCol]
                if endPiece == ' ':  # empty space valid
                    if self.checkFutureBoi(r, c, endRow, endCol):
                        self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                        self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [endRow, endCol]))
                elif (endPiece.islower() and startPiece.isupper() and self.squareSet[r][c].isupper()) or (
                        endPiece.isupper() and startPiece.islower() and self.squareSet[r][c].islower()):
                    # enemy piece is valid
                    if self.checkFutureBoi(r, c, endRow, endCol):
                        self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                        self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [endRow, endCol]))

    def bishop(self, r, c):
        startPiece = self.squareSet[r][c]
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.squareSet[endRow][endCol]
                    if endPiece == ' ':  # empty space valid
                        if self.checkFutureBoi(r, c, endRow, endCol):
                            self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                            self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [endRow, endCol]))
                    elif (endPiece.islower() and startPiece.isupper() and self.squareSet[r][c].isupper()) or (
                            endPiece.isupper() and startPiece.islower() and self.squareSet[r][c].islower()):
                        # enemy piece is valid
                        if self.checkFutureBoi(r, c, endRow, endCol):
                            self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                            self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [endRow, endCol]))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # out of board
                    break

    def queen(self, r, c):
        self.rook(r, c)
        self.bishop(r, c)

    def king(self, r, c):
        startPiece = self.squareSet[r][c]
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                endPiece = self.squareSet[endRow][endCol]
                if endPiece == ' ':  # empty space valid
                    if self.checkFutureBoi(r, c, endRow, endCol):
                        self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                        self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [endRow, endCol]))
                elif (endPiece.islower() and startPiece.isupper() and self.squareSet[r][c].isupper()) or (
                        endPiece.isupper() and startPiece.islower() and self.squareSet[r][c].islower()):
                    # enemy piece is valid
                    if self.checkFutureBoi(r, c, endRow, endCol):
                        self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                        self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [endRow, endCol]))

    def pawn(self, r, c):
        if self.squareSet[r][c].isupper():  # light pawn moves
            if r - 1 >= 0:
                if self.squareSet[r - 1][c] == ' ':
                    if self.checkFutureBoi(r, c, r - 1, c):
                        self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                        self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [r - 1, c]))
                    if r - 2 >= 0:
                        if r == 6 and self.squareSet[r - 2][c] == ' ':
                            if self.checkFutureBoi(r, c, r - 2, c):
                                self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                                self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [r - 2, c]))
            else:  # Promotion
                self.pawnPromotion(r, c)
            if c - 1 >= 0 and r - 1 >= 0:  # capture to the left
                if self.squareSet[r - 1][c - 1].islower() and self.squareSet[r][c].isupper():  # enemy piece to capture
                    if self.checkFutureBoi(r, c, r - 1, c - 1):
                        self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                        self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [r - 1, c - 1]))
                # En passant 1.Free space 2.Move acceptable 3.Pawn nearby
                if self.squareSet[r - 1][c - 1] == ' ' and self.GS.isEnPassantD[c - 1] \
                        and self.squareSet[r][c - 1] == 'p':  # en passant to the left
                    if self.checkFutureBoi(r, c, r - 1, c - 1):
                        self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                        self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [r - 1, c - 1]))
            if c + 1 <= 7 and r - 1 >= 0:  # capture to the right
                if self.squareSet[r - 1][c + 1].islower() and self.squareSet[r][c].isupper():  # enemy piece to capture
                    if self.checkFutureBoi(r, c, r - 1, c + 1):
                        self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                        self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [r - 1, c + 1]))
                # En passant 1.Free space 2.Move acceptable 3.Pawn nearby
                if self.squareSet[r - 1][c + 1] == ' ' and self.GS.isEnPassantD[c + 1] \
                        and self.squareSet[r][c + 1] == 'p':  # en passant to the right
                    if self.checkFutureBoi(r, c, r - 1, c + 1):
                        self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                        self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [r - 1, c + 1]))

        else:  # dark pawn moves
            if r + 1 < 8:
                if self.squareSet[r + 1][c] == ' ':
                    if self.checkFutureBoi(r, c, r + 1, c):
                        self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                        self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [r + 1, c]))
                    if r + 2 < 8:
                        if r == 1 and self.squareSet[r + 2][c] == ' ':
                            if self.checkFutureBoi(r, c, r + 2, c):
                                self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                                self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [r + 2, c]))
            else:  # Promotion
                self.pawnPromotion(r, c)
            if c - 1 >= 0 and r + 1 < 8:  # capture to the left
                if self.squareSet[r + 1][c - 1].isupper() and self.squareSet[r][c].islower():  # enemy piece to capture
                    if self.checkFutureBoi(r, c, r + 1, c - 1):
                        self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                        self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [r + 1, c - 1]))
                # En passant 1.Free space 2.Move acceptable 3.Pawn nearby
                if self.squareSet[r + 1][c - 1] == ' ' and self.GS.isEnPassantL[c - 1] \
                        and self.squareSet[r][c - 1] == 'P':  # en passant to the left
                    if self.checkFutureBoi(r, c, r + 1, c - 1):
                        self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                        self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [r + 1, c - 1]))
            if c + 1 <= 7 and r + 1 < 8:  # capture to the right
                if self.squareSet[r + 1][c + 1].isupper() and self.squareSet[r][c].islower():  # enemy piece to capture
                    if self.checkFutureBoi(r, c, r + 1, c + 1):
                        self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                        self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [r + 1, c + 1]))
                # En passant 1.Free space 2.Move acceptable 3.Pawn nearby
                if self.squareSet[r + 1][c + 1] == ' ' and self.GS.isEnPassantL[c + 1] \
                        and self.squareSet[r][c - 1] == 'P':  # en passant to the right
                    if self.checkFutureBoi(r, c, r + 1, c + 1):
                        self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                        self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [r + 1, c + 1]))

    def separateMoves(self):
        for i, j in zip(self.GS.validMovesFrom, self.GS.validMovesTo):
            if self.squareSet[i[0]][i[1]].islower():
                self.GS.validMovesFromDark = np.vstack((self.GS.validMovesFromDark, i))
                self.GS.validMovesToDark = np.vstack((self.GS.validMovesToDark, j))
            elif self.squareSet[i[0]][i[1]].isupper():
                self.GS.validMovesFromLight = np.vstack((self.GS.validMovesFromLight, i))
                self.GS.validMovesToLight = np.vstack((self.GS.validMovesToLight, j))

    def shortCastling(self, r, c):
        r = 7 if self.squareSet[r][c].isupper() else 0
        c = 4
        kingNotAvailable = []
        try:
            kingNotAvailable = self.GS.stackFrom.index([r, c])
        except ValueError:
            kingNotAvailable = []
        if not kingNotAvailable:
            rookNotAvailable = []
            try:
                rookNotAvailable = self.GS.stackFrom.index([r, c + 3])
            except ValueError:
                rookNotAvailable = []
                if not rookNotAvailable:
                    path = [self.squareSet[r][c + 1], self.squareSet[r][c + 2]]
                    clearPath = all(ele == ' ' for ele in path)
                    if clearPath:
                        if self.shortCastlingPathSafety(r, c):
                            self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                            self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [r, c + 2]))

    def shortCastlingPathSafety(self, r, c):
        fColCords = [r, c + 1]
        gColCords = [r, c + 2]

        if self.GS.side == 'l':
            fSafe = np.any(np.all(np.where(fColCords == self.GS.validMovesToDark, True, False), axis=1))
            gSafe = np.any(np.all(np.where(gColCords == self.GS.validMovesToDark, True, False), axis=1))
            if fSafe or gSafe:
                return False
        else:
            fSafe = np.any(np.all(np.where(fColCords == self.GS.validMovesToLight, True, False), axis=1))
            gSafe = np.any(np.all(np.where(gColCords == self.GS.validMovesToLight, True, False), axis=1))
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
                            self.GS.validMovesFrom = np.vstack((self.GS.validMovesFrom, [r, c]))
                            self.GS.validMovesTo = np.vstack((self.GS.validMovesTo, [r, c - 2]))

    def longCastlingPathSafety(self, r, c):
        cColCords = [r, c - 1]
        dColCords = [r, c - 2]

        if self.GS.side == 'l':
            fSafe = np.any(np.all(np.where(cColCords == self.GS.validMovesToDark, True, False), axis=1))
            gSafe = np.any(np.all(np.where(dColCords == self.GS.validMovesToDark, True, False), axis=1))
            if fSafe or gSafe:
                return False
        else:
            fSafe = np.any(np.all(np.where(cColCords == self.GS.validMovesToLight, True, False), axis=1))
            gSafe = np.any(np.all(np.where(dColCords == self.GS.validMovesToLight, True, False), axis=1))
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

    def checkCheck(self, r, c):
        # Light king
        if self.squareSet[r][c].isupper():
            kingSafe = np.any(np.all(np.where([r, c] == self.GS.validMovesToDark, True, False), axis=1))
            if kingSafe:
                return True
        # Dark King
        if self.squareSet[r][c].islower():
            kingSafe = np.any(np.all(np.where([r, c] == self.GS.validMovesToLight, True, False), axis=1))
            if kingSafe:
                return True
        return False

    def checkMate(self, r, c):
        # Is king under attack
        attacked = False
        # Possibility of moving to unattacked square
        runToFreedom = True
        # Light king
        if self.squareSet[r][c].isupper():
            attacked = np.any(np.all(np.where([r, c] == self.GS.validMovesToDark, True, False), axis=1))
            if attacked:
                runToFreedom = np.any(np.all(np.where([r, c] == self.GS.validMovesFromLight, True, False), axis=1))
        # Dark King
        if self.squareSet[r][c].islower():
            attacked = np.any(np.all(np.where([r, c] == self.GS.validMovesToLight, True, False), axis=1))
            if attacked:
                runToFreedom = np.any(np.all(np.where([r, c] == self.GS.validMovesFromDark, True, False), axis=1))

        # kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        # for i in range(8):
        #     endRow = r + kingMoves[i][0]
        #     endCol = c + kingMoves[i][1]
        #     if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board / not allay
        #         # Light King and end-square free or enemy
        #         if side and not self.squareSet[endRow][endCol].isupper():
        #             if np.any(np.all(np.where([endRow, endCol] == self.GS.validMovesToDark, True, False), axis=1)):
        #                 runToFreedom.append(False)
        #             else:
        #                 runToFreedom.append(True)
        #         # Dark King and end-square free or enemy
        #         elif side and not self.squareSet[endRow][endCol].islower():
        #             if np.any(np.all(np.where([endRow, endCol] == self.GS.validMovesToLight, True, False), axis=1)):
        #                 runToFreedom.append(False)
        #             else:
        #                 runToFreedom.append(True)
        # runToFreedom = True if np.any(runToFreedom) else False

        # Possibility of interposing
        if True:
            pass
            # Possibility of capturing threatening piece
            if True:
                pass

        if runToFreedom:
            return False
        else:
            return True

    def pawnPromotion(self, r, c):
        # Light pawn
        if self.squareSet[r][c].isupper():
            self.GS.isPromotionL[c] = False
        # Dark pawn
        else:
            self.GS.isPromotionD[c] = True

    def move(self, startRow, startCol, endRow, endCol):
        # Report an en Passant availability or reset it
        self.enPassantReport(startRow, startCol, endRow, endCol)
        # Proceed an en Passant
        if self.squareSet[endRow][endCol] == ' ' and endCol != startCol \
                and self.squareSet[startRow][startCol].lower() == 'p':
            if self.GS.side == 'l':
                self.squareSet[endRow + 1][endCol] = ' '
            else:
                self.squareSet[endRow - 1][endCol] = ' '
        # Proceed short castling
        if self.squareSet[startRow][startCol].lower() == 'k' and endCol == startCol + 2:
            self.squareSet[endRow][endCol - 1] = self.squareSet[endRow][endCol + 1]
            self.squareSet[endRow][endCol + 1] = ' '
        # Proceed long castling
        if self.squareSet[startRow][startCol].lower() == 'k' and endCol == startCol - 2:
            self.squareSet[endRow][endCol + 1] = self.squareSet[endRow][endCol - 2]
            self.squareSet[endRow][endCol - 2] = ' '

        # Always [target = piece] and [start = ' ']
        self.squareSet[endRow][endCol] = self.squareSet[startRow][startCol]
        self.squareSet[startRow][startCol] = ' '

        # # Update valid moves for checkmate
        # self.genValidMoves()
        # # Light king check update
        # self.GS.checkKingL = self.checkCheck(self.GS.kingLLoc[0], self.GS.kingLLoc[1])
        # # Dark king check update
        # self.GS.checkKingD = self.checkCheck(self.GS.kingDLoc[0], self.GS.kingDLoc[1])
        # Light king mate update
        # if self.GS.side == 'd':
        #     self.GS.mateKingL = self.checkMate(self.GS.kingLLoc[0], self.GS.kingLLoc[1])
        # # Dark king mate update
        # else:
        #     self.GS.mateKingD = self.checkMate(self.GS.kingDLoc[0], self.GS.kingDLoc[1])

        return list(np.array(self.squareSet).flatten())

    def checkFutureBoi(self, startRow, startCol, endRow, endCol):
        # King is dead
        if self.squareSet[endRow][endCol].lower() == 'k':
            return True
        if self.GS.testIteration:
            color = 'l' if self.squareSet[startRow][startCol].isupper() else 'd'
            backUpStat = copy.copy(self.GS)
            backUpBoard = list(np.array(self.squareSet).flatten())
            tempBoard = self.move(startRow, startCol, endRow, endCol)
            self.GS.stackFrom.append([startRow, startCol])
            self.GS.stackTo.append([endRow, endCol])
            self.GS.testIteration = False
            self.__init__(tempBoard, self.GS)
            # Update valid moves for checkmate
            self.genValidMoves()
            # Light king check update
            if color == 'l':
                self.GS.checkKingL = self.checkCheck(self.GS.kingLLoc[0], self.GS.kingLLoc[1])
                if self.GS.checkKingL:
                    self.__init__(backUpBoard, backUpStat)
                    del backUpStat
                    return False
                else:
                    self.__init__(backUpBoard, backUpStat)
                    del backUpStat
                    return True
            # Dark king check update
            else:
                self.GS.checkKingD = self.checkCheck(self.GS.kingDLoc[0], self.GS.kingDLoc[1])
                if self.GS.checkKingD:
                    self.__init__(backUpBoard, backUpStat)
                    del backUpStat
                    return False
                else:
                    self.__init__(backUpBoard, backUpStat)
                    del backUpStat
                    return True
        else:
            return True


