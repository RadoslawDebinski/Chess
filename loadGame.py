from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QGroupBox, QPushButton, QTextEdit, QMenu
from PyQt5.QtGui import QPixmap, QBrush
from PyQt5.QtCore import QPoint, pyqtSignal

from PyQt5 import uic
import sys
from PyQt5.QtCore import QPoint, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from chessBoard import ChessBoard
from stockEngine import StockEngine
import chessGraphics

stockPath = "C:\\Users\\radek\\Downloads\\stockfish-11-win\\stockfish-11-win\\Windows\\stockfish_20011801_x64.exe"


class UI(QMainWindow):
    def __init__(self, variant):
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

        self.variant = variant
        engine = StockEngine(stockPath)
        boardSet = engine.getPureBoard()
        self.boardSet = boardSet

        self.view = QGraphicsView(self)
        board = ChessBoard(self.boardSet, self.variant, self)
        self.view.setScene(board)
        self.view.setRenderHint(QPainter.Antialiasing)
        imgPath = f":/board/{self.variant}"
        pixmap = QPixmap(imgPath)
        self.view.setBackgroundBrush(QBrush(pixmap))
        self.view.setFixedSize(802, 802)

        # Create a QVBoxLayout object and add the view to it
        vbox = QVBoxLayout()
        vbox.addWidget(self.view)

        # Set the layout for the board QGroupBox
        self.board.setLayout(vbox)

        # Set up right-click menu for ChessBoard
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.showContextMenu)

        # Show the app
        self.show()

    def on_piece_released(self, boardSet):
        # print(f"Piece released at position:{int(newPos.x() / 100)}, {int(newPos.y() / 100)}")
        self.boardSet = boardSet
        self.view.setScene(ChessBoard(self.boardSet, self.variant, self))

    def showContextMenu(self, pos):
        # Create right-click menu with rotate options
        menu = QMenu(self)
        changeBoardStyle = menu.addAction("Change board style")

        # Show the menu and get the selected option
        action = menu.exec_(self.view.mapToGlobal(pos))

        # Call the appropriate rotate method based on the selected option
        if action == changeBoardStyle:
            self.changeBoardStyle()

    def changeBoardStyle(self):
        # Change the ChessBoard background color
        if self.variant == 's':
            self.variant = 'a'
            imgPath = f":/board/{self.variant}"
            pixmap = QPixmap(imgPath)
            self.view.setBackgroundBrush(QBrush(pixmap))
        else:
            self.variant = 's'
            imgPath = f":/board/{self.variant}"
            pixmap = QPixmap(imgPath)
            self.view.setBackgroundBrush(QBrush(pixmap))

        # Reload the ChessBoard with the new background color
        engine = StockEngine(stockPath)
        boardSet = engine.getPureBoard()
        self.boardSet = boardSet
        self.view.setScene(ChessBoard(self.boardSet, self.variant, self))


# Initialize the App
if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = UI('s')
    app.exec_()
