from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from chessPiece import ChessPiece
from PyQt5.QtCore import QPoint, pyqtSignal


class ChessBoard(QGraphicsScene):
    # Add this signal definition
    rightClicked = pyqtSignal(QPointF)

    def __init__(self, boardset, variant, UI, GS):
        super().__init__()
        self.boardSet = boardset
        self.setSceneRect(0, 0, 800, 800)
        self.variant = variant
        self.chessPieces = []

        cordX = 0
        cordY = 0
        # Locating pieces on board
        for pieceType in self.boardSet:
            chessPiece = ChessPiece(pieceType, cordX, cordY, self.variant, self.boardSet, UI, GS)
            self.chessPieces.append(chessPiece)
            self.addItem(chessPiece)
            cordX += 1
            if cordX == 8:
                cordX = 0
                cordY += 1

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.rightClicked.emit(event.scenePos())
        else:
            super().mousePressEvent(event)
