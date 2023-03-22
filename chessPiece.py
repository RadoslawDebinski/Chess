from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class ChessPiece(QGraphicsItem):
    def __init__(self, name, x, y):
        super().__init__()
        self.name = name
        self.x = x * 100 + 20
        self.y = y * 100 + 20
        color = ''

        if name == ' ':
            name = 'v'
            color = 'l'
        elif self.name.islower():
            color = 'd'
        else:
            color = 'l'

        imgPath = "chesspieces\\Chess_" + name.lower() + color + "t60.png"
        self.image = QImage(imgPath)

    def boundingRect(self):
        return QRectF(self.x, self.y, 100, 100)

    def paint(self, painter, option, widget):
        painter.drawImage(self.x, self.y, self.image)
