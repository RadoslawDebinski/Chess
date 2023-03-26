from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import chessGraphics
from chessEngine import ChessEngine
import numpy as np


class ChessPiece(QGraphicsItem):
    def __init__(self, name, x, y, variant, boardSet, UI):
        super().__init__()
        self.UI = UI
        self.name = name
        self.x = x
        self.y = y
        self.windX = x * 100 + 20
        self.windY = y * 100 + 20
        self.variant = variant
        self.boardSet = boardSet
        self.color = ''
        self.image = QImage()
        self.setFlag(QGraphicsItem.ItemIsMovable)

        # Setting piece color by letter size
        if self.name == ' ':
            self.name = 'v'
            self.color = 'l'
        elif self.name.islower():
            self.color = 'd'
        else:
            self.color = 'l'

        # Setting piece image
        imgPath = f":/{self.color}{self.variant}/{self.name.lower()}"
        self.image = QImage(imgPath)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)
            # Generate list of all valid moves
            engine = ChessEngine(self.boardSet)
            engine.isValid("", self.color)
            movesFrom = engine.getValidMovesFrom()

            pieceLoc = np.array([self.y, self.x])
            i = 0
            fromIdx = []
            # Finding indexes of valid moves for our piece
            for loc in movesFrom:
                if loc[0] == pieceLoc[0] and loc[1] == pieceLoc[1]:
                    fromIdx.append(i)
                i += 1
            # Generating all valid coordinates for piece move
            movesTo = engine.getValidMovesTo()
            movesTo = np.take(movesTo, fromIdx, axis=0)
            # Showing hints for user
            self.UI.showHints(movesTo)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.OpenHandCursor)
            # Move the chess piece to the new position
            newPos = event.scenePos()
            # Hiding user hints
            self.UI.hideHints()

            if self.isValidPosition(newPos):
                self.UI.on_piece_released(self.boardSet)

    def isValidPosition(self, newPos):
        # Check if the new position is within the bounds of the chessboard
        if newPos.x() < 0 or newPos.y() < 0 or newPos.x() > 800 or newPos.y() > 800:
            return False

        prevPosIdx = int(self.windX / 100)
        prevPosIdy = int(self.windY / 100)
        newPosIdx = int(newPos.x() / 100)
        newPosIdy = int(newPos.y() / 100)

        newBoardSet = self.boardSet
        targetField = newBoardSet[newPosIdy * 8 + newPosIdx]
        newBoardSet[newPosIdy * 8 + newPosIdx] = newBoardSet[prevPosIdy * 8 + prevPosIdx]
        newBoardSet[prevPosIdy * 8 + prevPosIdx] = targetField

        self.boardSet = newBoardSet

        return True


    def boundingRect(self):
        return QRectF(self.windX, self.windY, 100, 100)

    def paint(self, painter, option, widget):
        painter.drawImage(self.windX, self.windY, self.image)
