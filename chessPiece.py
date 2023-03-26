from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import chessGraphics

class ChessPiece(QGraphicsItem):
    def __init__(self, name, x, y, variant, boardSet, UI):
        super().__init__()
        self.UI = UI
        self.name = name
        self.x = x * 100 + 20
        self.y = y * 100 + 20
        self.variant = variant
        self.boardSet = boardSet
        self.color = ''
        self.image = QImage()
        self.setFlag(QGraphicsItem.ItemIsMovable)


        if self.name == ' ':
            self.name = 'v'
            self.color = 'l'
        elif self.name.islower():
            self.color = 'd'
        else:
            self.color = 'l'

        imgPath = f":/{self.color}{self.variant}/{self.name.lower()}"
        self.image = QImage(imgPath)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.OpenHandCursor)
            # Move the chess piece to the new position
            newPos = event.scenePos()

            # print(f"Position:{int(newPos.x() / 100)}, {int(newPos.y() / 100)}")
            if self.isValidPosition(newPos):
                self.UI.on_piece_released(self.boardSet)




    def isValidPosition(self, newPos):
        # Check if the new position is within the bounds of the chessboard
        if newPos.x() < 0 or newPos.y() < 0 or newPos.x() > 800 or newPos.y() > 800:
            return False

        prevPosIdx = int(self.x / 100)
        prevPosIdy = int(self.y / 100)
        newPosIdx = int(newPos.x() / 100)
        newPosIdy = int(newPos.y() / 100)

        newBoardSet = self.boardSet
        targetField = newBoardSet[newPosIdy * 8 + newPosIdx]
        newBoardSet[newPosIdy * 8 + newPosIdx] = newBoardSet[prevPosIdy * 8 + prevPosIdx]
        newBoardSet[prevPosIdy * 8 + prevPosIdx] = targetField

        self.boardSet = newBoardSet

        return True

    def rook(self):
        pass

    def knight(self):
        pass

    def bishop(self):
        pass

    def queen(self):
        pass

    def king(self):
        pass

    def pawn(self):
        pass

    def void(self):
        pass

    def boundingRect(self):
        return QRectF(self.x, self.y, 100, 100)

    def paint(self, painter, option, widget):
        painter.drawImage(self.x, self.y, self.image)
