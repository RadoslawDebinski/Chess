import chess
import chess.engine
import time
import numpy as np
from threading import Thread
from gameModes.stockEngine import StockEngine


# stockPath = "..\\stockfish-11-win\\Windows\\stockfish_20011801_x64.exe"
stockPath = "..\\stockfish_15.1_win_x64_avx2\\stockfish-windows-2022-x86-64-avx2.exe"


class Creator:
    def __init__(self, destinationPath, noThreads=12, threadPackages=7, packageSize=6140):
        self.input = np.array([])
        self.output = np.array([])
        self.destinationPath = destinationPath
        self.threadPackages = threadPackages
        self.packageSize = packageSize

        start_time = time.time()
        threads = []
        for i in range(noThreads):
            name = f'thread{i}_'
            t = Thread(target=self.threadFunc, args=(name,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        end_time = time.time()
        print(f'It took {end_time- start_time} second(s) to complete.')

    def threadFunc(self, threadName):
        for _ in range(self.threadPackages):
            inputData = np.array([])
            outputData = np.array([])
            inputData, outputData = self.createDataBase(self.packageSize, inputData, outputData)
            self.createFile(threadName, inputData, outputData)

    def randomBoard(self, maxDepth=200):
        board = chess.Board()
        depth = np.random.randint(0, maxDepth)
        for _ in range(depth):
            allMoves = list(board.legal_moves)
            randomMove = np.random.choice(allMoves)
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
        return engine.getEvaluation(fen)['value']

    def createFile(self, threadName, inputData, outputData):
        filePath = f'{self.destinationPath}\\{threadName}_{time.strftime("%Y%m%d-%H%M%S")}.npz'
        with open(filePath, 'wb') as f:
            np.save(f, inputData)
            np.save(f, outputData)

    def createDataBase(self, length, inputData, outputData):
        inputData = np.zeros((length, 4, 8, 8), dtype=np.int8)
        outputData = np.zeros(length, dtype=np.int8)

        inputData, outputData = zip(*[self.splitEvaluate() for _ in range(length)])
        inputData = np.array(inputData, dtype=np.int8)
        outputData = np.array(outputData, dtype=np.int8)
        return inputData, outputData

    def splitEvaluate(self):
        board = self.randomBoard()
        fen = board.fen()
        evaluation = self.stockfish(fen)
        if evaluation == 0:
            return self.splitEvaluate()
        board = self.splitBoard(board)
        return board, evaluation


if __name__ == '__main__':
    Creator('data3')
