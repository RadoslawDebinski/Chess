from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import chessGraphics

class ChessPiece(QGraphicsItem):
    def __init__(self, name, x, y, variant):
        super().__init__()
        self.name = name
        self.x = x * 100 + 20
        self.y = y * 100 + 20
        self.color = ''
        self.image = QImage()
        self.variant = variant

        if self.name == ' ':
            self.name = 'v'
            self.color = 'l'
        elif self.name.islower():
            self.color = 'd'
        else:
            self.color = 'l'

        imgPath = f":/{self.color}{self.variant}/{self.name.lower()}"
        self.image = QImage(imgPath)

        match self.name.lower():
            case 'r':
                self.rook()
            case 'n':
                self.knight()
            case 'b':
                self.bishop()
            case 'q':
                self.queen()
            case 'k':
                self.king()
            case 'p':
                self.pawn()
            case 'v':
                self.void()
        # imgPath = "chesspieces\\Chess_" + name.lower() + self.color + self.variant + "60.png"
        # self.image = QImage(imgPath)

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
