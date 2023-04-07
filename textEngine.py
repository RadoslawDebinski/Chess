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
        if len(data) == 0:
            return False
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

    # def algebraic_to_long_notation(self, move):
    #     pieces = {'K': 'King', 'Q': 'Queen', 'R': 'Rook', 'B': 'Bishop', 'N': 'Knight'}
    #     files = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    #     ranks = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    #
    #     # Determine if the move is a castling move
    #     if move in ['O-O', 'O-O-O', '0-0', '0-0-0']:
    #         return move.replace('-', ' ')  # Return the castling notation
    #
    #     # Determine the piece being moved
    #     if move[0] in pieces:
    #         piece = pieces[move[0]]
    #         start_index = 1
    #     else:
    #         piece = 'Pawn'
    #         start_index = 0
    #
    #     # Determine the starting square of the piece being moved
    #     if 'x' in move:
    #         start_file = files[move[start_index - 1]]
    #         start_rank = ranks[move[start_index + 1]]
    #     else:
    #         start_file = files[move[start_index]]
    #         start_rank = ranks[move[start_index + 1]]
    #
    #     # Determine the destination square
    #     destination_file = files[move[start_index]]
    #     destination_rank = ranks[move[start_index + 1]]
    #     destination = f"{destination_file}, {destination_rank}"
    #
    #     # Determine if the move is a capture or check
    #     if '#' in move:
    #         check = 'checkmate'
    #     elif '+' in move:
    #         check = 'check'
    #     else:
    #         check = None
    #
    #     # Determine if the move is a capture
    #     if 'x' in move:
    #         capture = True
    #         capture_square = f"{destination_file}, {start_rank}"
    #         return f"{piece} on {start_file}, {start_rank} captures on {capture_square} and moves to {destination} {check}"
    #
    #     # Determine if the move is a pawn promotion
    #     if len(move) == 5 and move[4] in pieces:
    #         promotion_piece = pieces[move[4]]
    #         return f"{piece} on {start_file}, {start_rank} moves to {destination} and promotes to a {promotion_piece} {check}"
    #
    #     # Determine if the move is en passant
    #     if 'e.p.' in move:
    #         capture_file = files[move[start_index]]
    #         capture_rank = int(move[start_index + 1]) - 1 if piece == 'Pawn' else int(move[start_index + 1]) + 1
    #         capture_square = f"{capture_file}, {capture_rank}"
    #         return f"{piece} on {start_file}, {start_rank} captures en passant on {capture_square} and moves to {destination} {check}"
    #
    #     # If none of the above conditions are met, it's a regular move
    #     return f"{piece} on {start_file}, {start_rank} moves to {destination} {check}"

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


