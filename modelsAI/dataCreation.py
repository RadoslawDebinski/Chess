import chess
import chess.engine
import random
import time
import numpy as np
from gameModes.stockEngine import StockEngine


stockPath = "..\\stockfish-11-win\\Windows\\stockfish_20011801_x64.exe"

class Creator:
    def __init__(self):
        self.input = np.array([])
        self.output = np.array([])
        self.visual = []
        self.createDataBase()
        self.createFile()

    def randomBoard(self, maxDepth=200):
        board = chess.Board()
        depth = random.randrange(0, maxDepth)

        for _ in range(depth):
            allMoves = list(board.legal_moves)
            randomMove = random.choice(allMoves)
            board.push(randomMove)
            if board.is_game_over():
                break

        return board

    def splitBoard(self, board):
        boardOut = np.zeros((4, 8, 8), dtype=np.int8)

        translationL = {
            1: [0, 0, 0, 1],
            2: [0, 0, 1, 0],
            3: [0, 0, 1, 1],
            4: [0, 1, 0, 0],
            5: [0, 1, 0, 1],
            6: [0, 1, 1, 0]
        }

        translationD = {
            1: [1, 0, 0, 1],
            2: [1, 0, 1, 0],
            3: [1, 0, 1, 1],
            4: [1, 1, 0, 0],
            5: [1, 1, 0, 1],
            6: [1, 1, 1, 0]
        }

        for piece in chess.PIECE_TYPES:
            for square in board.pieces(piece, chess.WHITE):
                idx = np.unravel_index(square, (8, 8))
                boardOut[:, 7 - idx[0], idx[1]] = translationL[piece]

            for square in board.pieces(piece, chess.BLACK):
                idx = np.unravel_index(square, (8, 8))
                boardOut[:, 7 - idx[0], idx[1]] = translationD[piece]
        return boardOut

    def stockfish(self, fen):
        engine = StockEngine(stockPath)
        evaluation = engine.getEvaluation(fen)
        return engine.getEvaluation(fen)['value']

    def createFile(self):
        # with open('data\\test.npz', 'wb') as f:
        #     np.save(f, self.input)
        #     np.save(f, self.output)
        # with open('data\\test.npz', 'rb') as f:
        #     a = np.load(f)
        #     b = np.load(f)
        valid = np.count_nonzero(self.output)
        print(valid)

    def createDataBase(self, length=1):
        self.input = np.zeros((length, 4, 8, 8), dtype=np.int8)
        self.output = np.zeros(length, dtype=np.int8)

        self.input, self.output = zip(*[self.splitEvaluate() for _ in range(length)])
        self.input = np.array(self.input, dtype=np.int8)
        self.output = np.array(self.output, dtype=np.int8)

    def splitEvaluate(self):
        board = self.randomBoard()
        fen = board.fen()
        self.visual = board
        evaluation = self.stockfish(fen)
        board = self.splitBoard(board)
        return board, evaluation

if __name__ == '__main__':
    start = time.time()
    Creator()
    end = time.time()
    print(end-start)
