import os

import chess
import chess.engine
import itertools
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
        print(f'It took {end_time - start_time} second(s) to complete.')

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


class Translator:
    def __init__(self, sourcePath, destinationPath):
        self.sourcePath = sourcePath
        self.destinationPath = destinationPath
        self.noFiles = len(
            [entry for entry in os.listdir(sourcePath) if os.path.isfile(os.path.join(sourcePath, entry))])
        self.entries = os.listdir(sourcePath)
        start_time = time.time()
        self.x_data, self.y_data = self.get_data()
        print(f'Packages input shape: {np.shape(self.x_data)}')
        print(f'Packages output shape: {np.shape(self.y_data)}')

        self.translate()
        end_time = time.time()
        print(f'It took {end_time - start_time} second(s) to complete.')

    def get_data(self):
        x_train = []
        y_train = []
        for i in range(self.noFiles):
            with open(f'{self.sourcePath}\\{self.entries[i]}', 'rb') as f:
                packageInput = np.load(f)
                packageOutput = np.load(f)
                print(f'Package {self.entries[i]} input shape: {np.shape(packageInput)}')
                print(f'Package {self.entries[i]} output shape: {np.shape(packageOutput)}')
                x_train.append(packageInput)
                y_train.append(packageOutput)
        return np.concatenate(x_train, axis=0), np.concatenate(y_train, axis=0)

    def translate(self):
        print(np.shape(self.x_data))

        translation = {
            (0, 0, 0, 1): [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            (0, 0, 1, 0): [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            (0, 0, 1, 1): [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            (0, 1, 0, 0): [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            (0, 1, 0, 1): [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            (0, 1, 1, 0): [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],

            (1, 0, 0, 1): [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            (1, 0, 1, 0): [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            (1, 0, 1, 1): [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            (1, 1, 0, 0): [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            (1, 1, 0, 1): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            (1, 1, 1, 0): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],

            (0, 0, 0, 0): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        }
        for iter in range(1000):
            new_data = np.zeros((1, 13, 8, 8), dtype=np.int8)
            new_board = np.zeros((13, 8, 8), dtype=np.int8)

            translation_keys = list(translation.keys())
            translation_values = np.array(list(translation.values()))

            for t, board in enumerate(self.x_data[0+1000*iter:1000+1000*iter], start=1):
                for i, j in itertools.product(range(8), range(8)):
                    key = tuple(board[:, i, j])
                    idx = translation_keys.index(key)
                    new_board[:, i, j] = translation_values[idx]
                new_data = np.concatenate((new_data, [new_board]), axis=0)
                if t % 10000 == 0:
                    print(f'There is no.{t} boards now.')

            new_data = new_data[1:, :, :, :]
            self.create_file(new_data, self.y_data)

    def show_visual13(self, board):
        translation = {
            (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0): 'P',
            (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0): 'N',
            (0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0): 'B',
            (0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0): 'R',
            (0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0): 'Q',
            (0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0): 'K',
            (0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0): 'p',
            (0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0): 'n',
            (0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0): 'b',
            (0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0): 'r',
            (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0): 'q',
            (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0): 'k',
            (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1): 'v'
        }
        translation_keys = list(translation.keys())
        translation_values = np.array(list(translation.values()))

        new_board = np.chararray((8, 8))

        for i, j in itertools.product(range(8), range(8)):
            key = tuple(board[:, i, j])
            idx = translation_keys.index(key)
            new_board[i, j] = translation_values[idx]

        print(new_board)

    def create_file(self, inputData, outputData):
        filePath = f'{self.destinationPath}\\data_combined_{time.strftime("%Y%m%d-%H%M%S")}.npz'
        with open(filePath, 'wb') as f:
            np.save(f, inputData)
            np.save(f, outputData)


if __name__ == '__main__':
    # Creator('data3')
    Translator('C:\\aidata\\data3', 'C:\\aidata\\data_size_13_back')
