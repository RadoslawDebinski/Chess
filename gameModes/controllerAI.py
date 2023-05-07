import io
import itertools
import os
import tensorflow as ts
from tensorflow.keras import models
from core.chessEngine import ChessEngine
from gameModes.stockEngine import StockEngine
import numpy as np

class PlayerAI:
    def __init__(self, model, sEngine):
        self.model = models.load_model(r'C:\\aidata\\model.h5')
        self.engine = sEngine
        self.history = []
        self.bestMove = []
        self.boardSets = []

    def get_move_stockfish(self):
        self.engine.engine.make_moves_from_current_position(self.history)
        self.bestMove = self.engine.engine.get_best_move()
        print(self.bestMove)
        self.translate_from_stockfish()

    def translate_to_stockfish(self, movesFrom, movesTo):
        ranks = {7: '1', 6: '2', 5: '3', 4: '4', 3: '5', 2: '6', 1: '7', 0: '8'}
        files = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        self.history = []

        for moveFrom, moveTo in zip(movesFrom[1:], movesTo[1:]):
            self.history.append(f"{files[moveFrom[1]]}{ranks[moveFrom[0]]}{files[moveTo[1]]}{ranks[moveTo[0]]}")

    def translate_from_stockfish(self):
        ranks = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
        files = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        self.bestMove = [ranks[self.bestMove[1]], files[self.bestMove[0]],
                         ranks[self.bestMove[3]], files[self.bestMove[2]]]

    def get_model_boards(self, UI):
        validMovesFromDark = UI.GS.validMovesFromDark[1:]
        validMovesToDark = UI.GS.validMovesToDark[1:]
        boardSets = []
        for moveFrom, moveTo in zip(validMovesFromDark, validMovesToDark):
            engine = ChessEngine(UI.boardSet, UI.GS)
            boardSet, GS = engine.move(moveFrom[0], moveFrom[1], moveTo[0], moveTo[1])
            boardSets.append(boardSet)

        self.boardSets = self.translate_to_model_input(boardSets)

    def get_best_model_move(self, UI):
        # model = models.load_model(r'C:\\aidata\\model.h5')
        predictions = [self.model(np.array([board]))[0][0] for board in self.boardSets]
        predictions = np.array(predictions)
        moveIdx = np.argmin(predictions)
        bestMoveFrom = UI.GS.validMovesFromDark[moveIdx+1]
        bestMoveTo = UI.GS.validMovesToDark[moveIdx+1]
        self.bestMove = [bestMoveFrom[0], bestMoveFrom[1], bestMoveTo[0], bestMoveTo[1]]
        print(self.bestMove)

    def translate_to_model_input(self, boardSets):
        translation = {
            'P': (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            'N': (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            'B': (0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            'R': (0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            'Q': (0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0),
            'K': (0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0),
            'p': (0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0),
            'n': (0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0),
            'b': (0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0),
            'r': (0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0),
            'q': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0),
            'k': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0),
            ' ': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)
        }
        translation_keys = list(translation.keys())
        translation_values = np.array(list(translation.values()))

        new_boards = np.zeros((1, 13, 8, 8), dtype=np.int8)
        new_board = np.zeros((13, 8, 8), dtype=np.int8)
        boardLen = 8
        for board in boardSets:
            for i, j in itertools.product(range(8), range(8)):
                key = board[i * boardLen + j]
                idx = translation_keys.index(key)
                new_board[:, i, j] = translation_values[idx]
            new_boards = np.concatenate((new_boards, [new_board]), axis=0)

        return new_boards[1:, :, :, :]

    def move(self, boardSet, GS):
        prevRow, prevCol = self.bestMove[0], self.bestMove[1]
        newRow, newCol = self.bestMove[2], self.bestMove[3]
        engine = ChessEngine(boardSet, GS)
        boardSet, GS = engine.move(prevRow, prevCol, newRow, newCol)
        # Game stack update
        GS.stackFrom.append([prevRow, prevCol])
        GS.stackTo.append([newRow, newCol])
        GS.changeSide()
        # Report check
        GS.clearStatus()
        GS = engine.checkCheck(boardSet, GS)

        return boardSet, GS
