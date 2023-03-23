from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from chessPiece import ChessPiece


class ChessBoard(QGraphicsScene):
    def __init__(self, boardset, variant):
        super().__init__()
        self.boardSet = boardset
        self.setSceneRect(0, 0, 800, 800)
        self.variant = variant

        cordX = 0
        cordY = 0
        for pieceType in self.boardSet:
            self.addItem(ChessPiece(pieceType, cordX, cordY, self.variant))
            cordX += 1
            if cordX == 8:
                cordX = 0
                cordY += 1
