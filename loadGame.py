from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QGroupBox, QPushButton, QTextEdit
from PyQt5 import uic
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from chessBoard import ChessBoard
from stockEngine import StockEngine
import chessGraphics

stockPath = "C:\\Users\\radek\\Downloads\\stockfish-11-win\\stockfish-11-win\\Windows\\stockfish_20011801_x64.exe"

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the ui file
        uic.loadUi("loadui.ui", self)
        self.setWindowTitle("Chess Game")

        # Define Our Widgets
        self.board = self.findChild(QGroupBox, "BoardBox")
        self.clock1 = self.findChild(QGroupBox, "ClockBox1")
        self.clock2 = self.findChild(QGroupBox, "ClockBox2")
        self.textEdit = self.findChild(QTextEdit, "textEdit")
        self.submitButton = self.findChild(QPushButton, "SubmitButton")
        self.reverseButton = self.findChild(QPushButton, "ReverseButton")

        self.variant = 'a'
        engine = StockEngine(stockPath)
        boardSet = engine.getPureBoard()
        self.boardSet = boardSet

        view = QGraphicsView(self)
        view.setScene(ChessBoard(self.boardSet, self.variant))
        view.setRenderHint(QPainter.Antialiasing)
        imgPath = f":/board/{self.variant}"
        pixmap = QPixmap(imgPath)
        view.setBackgroundBrush(QBrush(pixmap))
        view.setFixedSize(802, 802)

        # Create a QVBoxLayout object and add the view to it
        vbox = QVBoxLayout()
        vbox.addWidget(view)

        # Set the layout for the board QGroupBox
        self.board.setLayout(vbox)

        # Show the app
        self.show()


# Initialize the App
if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()
