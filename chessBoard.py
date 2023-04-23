from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from chessPiece import ChessPiece
from PyQt5.QtCore import QPoint, pyqtSignal
import numpy as np


class ChessBoard(QGraphicsScene):
    # Add this signal definition
    rightClicked = pyqtSignal(QPointF)

    def __init__(self, boardset, variant, UI, GS):
        super().__init__()
        self.boardSet = boardset
        self.setSceneRect(0, 0, 800, 800)
        self.variant = variant

        cordX = 0
        cordY = 0
        # Locating pieces on board
        x, y = np.meshgrid(np.arange(8), np.arange(8))
        indexes = np.column_stack((x.ravel(), y.ravel()))
        self.pieces = []
        # [self.addItem(ChessPiece(pieceType, cords[0], cords[1], self.variant, self.boardSet, UI, GS)) for
        #  pieceType, cords in zip(self.boardSet, indexes)]

        for pieceType, cords in zip(self.boardSet, indexes):
            piece = ChessPiece(pieceType, cords[0], cords[1], self.variant, self.boardSet, UI, GS)
            self.addItem(piece)
            self.pieces.append(piece)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.rightClicked.emit(event.scenePos())
        else:
            super().mousePressEvent(event)
