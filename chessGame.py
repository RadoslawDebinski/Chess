from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from chessBoard import ChessBoard
from stockEngine import StockEngine

stockPath = "C:\\Users\\radek\\Downloads\\stockfish-11-win\\stockfish-11-win\\Windows\\stockfish_20011801_x64.exe"


class ChessGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 800)
        self.setWindowTitle("Chess Game")
        engine = StockEngine(stockPath)
        boardSet = engine.getPureBoard()
        self.boardSet = boardSet
        self.initUI()

    def initUI(self):
        view = QGraphicsView(self)
        view.setScene(ChessBoard(self.boardSet))
        view.setRenderHint(QPainter.Antialiasing)
        pixmap = QPixmap("chesspieces\\board1.png")
        view.setBackgroundBrush(QBrush(pixmap))
        view.setFixedSize(802, 802)
        self.setCentralWidget(view)
