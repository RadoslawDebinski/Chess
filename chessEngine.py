import numpy as np


class ChessEngine:
    def __init__(self, boardSet):
        self.boardSet = boardSet
        n = 8
        self.squareSet = [self.boardSet[i:i + n] for i in range(0, len(self.boardSet), n)]
        self.moveLongNot = ''
        self.moveShortNot = ''
        self.side = ''
        self.validMoves = np.empty([2, 1], dtype=int)

    def isValid(self, text, side):
        self.moveShortNot = text
        # here translation from short to long !!!
        self.moveLongNot = self.moveShortNot
        # here translation from long to indexes
        self.side = side
        self.genValidMoves()

    def genValidMoves(self):
        for r in range(len(self.squareSet)):
            for c in range(len(self.squareSet[r])):
                match self.squareSet[r][c]:
                    case 'r':
                        self.rook(r, c)
                    case 'n':
                        self.knight(r, c)
                    case 'b':
                        self.bishop(r, c)
                    case 'q':
                        self.queen(r, c)
                    case 'k':
                        self.king(r, c)
                    case 'p':
                        self.pawn(r, c)
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
                        self.validMoves[0] = np.append(self.validMoves[0], [r, c]), self.validMoves[1] = np.append(self.validMoves[1], [endRow, endCol])
                    elif (endPiece.islower() and self.side == 'l') or (endPiece.isupper() and self.side != 'l'):
                        # enemy piece is valid
                        self.validMoves[0] = np.append(self.validMoves[0], [r, c]), self.validMoves[1] = np.append(self.validMoves[1], [endRow, endCol])
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
                    self.validMoves[0] = np.append(self.validMoves[0], [r, c]), self.validMoves[1] = np.append(self.validMoves[1], [endRow, endCol])
                elif (endPiece.islower() and self.side == 'l') or (endPiece.isupper() and self.side != 'l'):
                    # enemy piece is valid
                    self.validMoves[0] = np.append(self.validMoves[0], [r, c]), self.validMoves[1] = np.append(self.validMoves[1], [endRow, endCol])
                    break
                else:  # friendly piece invalid
                    break
            else:  # out of board
                break

    def bishop(self, r, c):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.squareSet[endRow][endCol]
                    if endPiece == ' ':  # empty space valid
                        self.validMoves[0] = np.append(self.validMoves[0], [r, c]), self.validMoves[1] = np.append(self.validMoves[1], [endRow, endCol])
                    elif (endPiece.islower() and self.side == 'l') or (endPiece.isupper() and self.side != 'l'):
                        # enemy piece is valid
                        self.validMoves[0] = np.append(self.validMoves[0], [r, c]), self.validMoves[1] = np.append(self.validMoves[1], [endRow, endCol])
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
                    self.validMoves[0] = np.append(self.validMoves[0], [r, c]), self.validMoves[1] = np.append(self.validMoves[1], [endRow, endCol])
                elif (endPiece.islower() and self.side == 'l') or (endPiece.isupper() and self.side != 'l'):
                    # enemy piece is valid
                    self.validMoves[0] = np.append(self.validMoves[0], [r, c]), self.validMoves[1] = np.append(self.validMoves[1], [endRow, endCol])
                    break
                else:  # friendly piece invalid
                    break
            else:  # out of board
                break

    def pawn(self, r, c):
        if self.side == 'l':  # light pawn moves
            if self.squareSet[r - 1][c] == ' ':
                self.validMoves[0] = np.append(self.validMoves[0], [r, c]), self.validMoves[1] = np.append(self.validMoves[1], [r - 1, c])
                if r == 6 and self.squareSet[r - 2][c] == ' ':
                    self.validMoves[0] = np.append(self.validMoves[0], [r, c]), self.validMoves[1] = np.append(self.validMoves[1], [r - 2, c])
            if c - 1 >= 0:  # capture to the left
                if self.squareSet[r - 1][c - 1].islower():  # enemy piece to capture
                    self.validMoves[0] = np.append(self.validMoves[0], [r, c]), self.validMoves[1] = np.append(self.validMoves[1], [r - 1, c - 1])
            if c + 1 <= 7:  # capture to the right
                if self.squareSet[r - 1][c + 1].islower():  # enemy piece to capture
                    self.validMoves[0] = np.append(self.validMoves[0], [r, c]), self.validMoves[1] = np.append(self.validMoves[1], [r - 1, c + 1])
        else:  # dark pawn moves
            if self.squareSet[r + 1][c] == ' ':
                self.validMoves[0] = np.append(self.validMoves[0], [r, c]), self.validMoves[1] = np.append(self.validMoves[1], [r + 1, c])
                if r == 1 and self.squareSet[r + 2][c] == ' ':
                    self.validMoves[0] = np.append(self.validMoves[0], [r, c]), self.validMoves[1] = np.append(self.validMoves[1], [r + 2, c])
            if c - 1 >= 0:  # capture to the left
                if self.squareSet[r + 1][c - 1].isupper:  # enemy piece to capture
                    self.validMoves[0] = np.append(self.validMoves[0], [r, c]), self.validMoves[1] = np.append(self.validMoves[1], [r + 1, c - 1])
            if c + 1 <= 7:  # capture to the right
                if self.squareSet[r + 1][c + 1].isupper():  # enemy piece to capture
                    self.validMoves[0] = np.append(self.validMoves[0], [r, c]), self.validMoves[1] = np.append(self.validMoves[1], [r + 1, c + 1])

    def move(self):
        pass
