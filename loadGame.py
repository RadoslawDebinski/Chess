from PyQt5.QtWidgets import QGroupBox, QPushButton, QTextEdit, QMenu
from PyQt5.QtGui import QPixmap, QBrush

from PyQt5 import uic
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from chessBoard import ChessBoard
from stockEngine import StockEngine
from chessEngine import ChessEngine
import chessGraphics
from gamesStatus import GameStatus
import time
from textEngine import TextEngine
from chessClock import ChessClock

stockPath = "stockfish-11-win\\Windows\\stockfish_20011801_x64.exe"


class UI(QMainWindow):
    def __init__(self, variant):
        super(UI, self).__init__()

        # Variables for hints
        hintPath = f":/hint/transparent"
        self.pixmap = QPixmap(hintPath)
        self.hints = []

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
        self.checkLight = self.findChild(QPushButton, "pushButton_4")
        self.checkDark = self.findChild(QPushButton, "pushButton")
        self.mateLight = self.findChild(QPushButton, "pushButton_3")
        self.mateDark = self.findChild(QPushButton, "pushButton_2")
        self.startButton = self.findChild(QPushButton, "startButton")
        self.resetButton = self.findChild(QPushButton, "resetButton")

        # Initial textEdit message
        self.textEdit.setText("Here insert move")
        # Create a QFont object with a larger font size
        font = QFont()
        font.setPointSize(28)
        # Set the font for the textEdit widget
        self.textEdit.setFont(font)

        # Connect our Widgets
        self.submitButton.clicked.connect(self.onSubmit)
        self.reverseButton.clicked.connect(self.onReverse)
        self.textEdit.textChanged.connect(self.onTextChanged)
        self.resetButton.clicked.connect(self.resetGame)
        self.startButton.clicked.connect(self.startGame)

        # Create an event loop
        # self.loop = QEventLoop()

        # Clocks
        self.clockDark = ChessClock()
        self.clockLight = ChessClock()

        # Clocks memory
        self.clockMemory = 'l'

        # Add clocks view, scene and add them to boxes
        self.clockViewDark = QGraphicsView(self)
        self.clockViewLight = QGraphicsView(self)
        clockSceneDark = QGraphicsScene(self)
        clockSceneLight = QGraphicsScene(self)
        clockSceneDark.addItem(self.clockDark)
        clockSceneLight.addItem(self.clockLight)
        self.clockViewDark.setScene(clockSceneDark)
        self.clockViewLight.setScene(clockSceneLight)
        clockBoxDark = QVBoxLayout()
        clockBoxLight = QVBoxLayout()
        clockBoxDark.addWidget(self.clockViewDark)
        clockBoxLight.addWidget(self.clockViewLight)
        self.clock1.setLayout(clockBoxDark)
        self.clock2.setLayout(clockBoxLight)

        # Initial board set
        self.variant = variant
        engine = StockEngine(stockPath)
        boardSet = engine.getPureBoard()
        self.boardSet = boardSet
        # Initial game status recorder
        self.GS = GameStatus()

        # Set board appearance
        self.view = QGraphicsView(self)
        board = ChessBoard(self.boardSet, self.variant, self, self.GS)

        # Generate list of all valid moves
        engine = ChessEngine(self.boardSet, self.GS)
        self.GS = engine.genValidMoves()

        self.view.setScene(board)
        self.view.setRenderHint(QPainter.Antialiasing)
        imgPath = f":/board/{self.variant}"
        pixmap = QPixmap(imgPath)
        self.view.setBackgroundBrush(QBrush(pixmap))
        self.view.setFixedSize(802, 802)

        # Locate and set labels
        labelAbcdPath = f":/label/abcd"
        label1234Path = f":/label/1234"
        pixmapAbcd = QPixmap(labelAbcdPath)
        pixmap1234 = QPixmap(label1234Path)
        # Create a QLabel widget and set the pixmap as its contents
        labelAbcd = QLabel(self)
        label1234 = QLabel(self)
        labelAbcd.setPixmap(pixmapAbcd)
        label1234.setPixmap(pixmap1234)
        # Set the position and size of the label
        labelAbcd.setGeometry(20, 869, 801, 31)
        label1234.setGeometry(828, 61, 31, 801)

        # Create a QVBoxLayout object and add the view to it
        vbox = QVBoxLayout()
        vbox.addWidget(self.view)

        # Set the layout for the board QGroupBox
        self.board.setLayout(vbox)

        # Set up right-click menu for ChessBoard
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.showContextMenu)

        # Disable all elements of scene other than start button
        self.disableScene()

        # Show the app
        self.show()

    def startGame(self):
        self.board.setEnabled(True)
        self.submitButton.setEnabled(True)
        self.textEdit.setEnabled(True)
        self.clockLight.timer.start(1)
        self.startButton.setEnabled(False)

    def resetGame(self):
        time.sleep(1)
        # Create a new instance of the UI class
        new_instance = UI(self.variant)
        # Close the current instance
        self.close()

    def disableScene(self):
        self.board.setEnabled(False)
        self.submitButton.setEnabled(False)
        self.textEdit.setEnabled(False)

    def onReverse(self):
        if self.GS.side == 'l':
            self.clockLight.timer.start(1)
            self.clockDark.timer.stop()
            self.clockMemory = 'd'
        else:
            self.clockLight.timer.stop()
            self.clockDark.timer.start(1)
            self.clockMemory = 'l'
        # Unable buttons
        # self.board.setEnabled(True)
        # self.submitButton.setEnabled(True)
        # self.textEdit.setEnabled(True)

        # Exit the event loop when the ReverseButton is clicked
        # if self.loop.isRunning():
        #     self.loop.exit()

    def onTextChanged(self):
        text = self.textEdit.toPlainText()
        if text.endswith("\n"):
            self.submitButton.click()

    def showHints(self, hintTo):
        # Clear any previously shown hints
        [hint.hide() for hint in self.hints]
        self.hints = []
        self.hints = [self.createHintLabel(hintCoord) for hintCoord in hintTo]

    def createHintLabel(self, hintCoord):
        hintLabel = QLabel(self.view)
        hintLabel.setPixmap(self.pixmap)
        hintLabel.setGeometry(QRect(hintCoord[1] * 100 + 23, hintCoord[0] * 100 + 23, 60, 60))
        hintLabel.show()
        return hintLabel

    def hideHints(self):
        for hint in self.hints:
            hint.hide()

    def onSubmit(self):
        # Get the text from the textEdit widget
        text = self.textEdit.toPlainText()
        engine = TextEngine(self.boardSet, self.GS)

        if engine.algebraicToLongNotation(text):
            valid, self.boardSet, self.GS = engine.isMoveValid()
            if valid:
                self.textEdit.clear()
                self.onPieceReleased(self.boardSet, self.GS)
            else:
                self.textEdit.clear()
                self.textEdit.setText("Unacceptable move insert new one")
        else:
            self.textEdit.clear()
            self.textEdit.setText("This is not valid move")

    def checkMates(self):
        if self.GS.checkKingL:
            self.checkLight.setStyleSheet('QPushButton {background-color: %s}' % QColor(255, 0, 0).name())
        else:
            self.checkLight.setStyleSheet('QPushButton {background-color: %s}' % QColor(0, 160, 255).name())
        self.checkLight.repaint()

        if self.GS.checkKingD:
            self.checkDark.setStyleSheet('QPushButton {background-color: %s}' % QColor(255, 0, 0).name())
        else:
            self.checkDark.setStyleSheet('QPushButton {background-color: %s}' % QColor(0, 160, 255).name())
        self.checkDark.repaint()
        if self.GS.mateKingL:
            self.mateLight.setStyleSheet('QPushButton {background-color: %s}' % QColor(255, 0, 0).name())
            self.mateLight.repaint()
            time.sleep(3)
            # Create a new instance of the UI class
            new_instance = UI(self.variant)
            # Close the current instance
            self.close()
        else:
            self.mateLight.setStyleSheet('QPushButton {background-color: %s}' % QColor(0, 160, 255).name())

        if self.GS.mateKingD:
            self.mateDark.setStyleSheet('QPushButton {background-color: %s}' % QColor(255, 0, 0).name())
            self.mateDark.repaint()
            time.sleep(3)
            # Create a new instance of the UI class
            new_instance = UI(self.variant)
            # Close the current instance
            self.close()
        else:
            self.mateDark.setStyleSheet('QPushButton {background-color: %s}' % QColor(0, 160, 255).name())
        self.mateLight.repaint()
        self.mateDark.repaint()

    def onPieceReleased(self, boardSet, GS):
        self.GS = GS
        self.boardSet = boardSet
        self.pawnPromotion()

        # Next Player
        self.GS.clearStatus()

        # Generate list of all valid moves
        engine = ChessEngine(self.boardSet, self.GS)
        self.GS = engine.genValidMoves()
        # Report Mates
        self.GS = engine.checkMates(self.GS)
        self.checkMates()
        self.view.setScene(ChessBoard(self.boardSet, self.variant, self, self.GS))
        # Disable all elements of scene other than onReverse button
        # self.disableScene()
        # Wait for the ReverseButton to be clicked
        # self.loop.exec()


    def showContextMenu(self, pos):
        # Create right-click menu with rotate options
        menu = QMenu(self)
        changeBoardStyle = menu.addAction("Change board style")

        # Show the menu and get the selected option
        action = menu.exec_(self.view.mapToGlobal(pos))

        # Call the appropriate rotate method based on the selected option
        if action == changeBoardStyle:
            self.changeBoardStyle()

    def pawnPromotion(self):
        if any(self.GS.isPromotionL):
            column = self.GS.isPromotionL.index(True)
            self.createMenu()
            if self.GS.newFig == 'K':
                self.GS.newFig = 'N'
            self.boardSet[column] = self.GS.newFig
            self.GS.isPromotionL[column] = False
        if any(self.GS.isPromotionD):
            column = self.GS.isPromotionD.index(True)
            self.createMenu()
            if self.GS.newFig == 'K':
                self.GS.newFig = 'N'
            self.boardSet[56 + column] = self.GS.newFig.lower()
            self.GS.isPromotionD[column] = False

    def createMenu(self):
        # Create a QDialog widget as our menu window
        promMenu = QDialog()
        promMenu.setWindowFlags(Qt.WindowCloseButtonHint)  # disable the close button

        # Create a QVBoxLayout to hold the buttons
        layout = QVBoxLayout()

        # Create four buttons and add them to the layout
        button1 = QPushButton("Queen")
        button2 = QPushButton("Rook")
        button3 = QPushButton("Bishop")
        button4 = QPushButton("Knight")
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(button4)

        # Set the layout for the menu window
        promMenu.setLayout(layout)

        # Define a callback function for when a button is clicked
        button_text = ""

        def on_button_click():
            # Get the text label of the clicked button
            self.GS.newFig = promMenu.sender().text()[0]
            # Close the menu window
            promMenu.hide()

        # Connect the callback function to each button's clicked signal
        button1.clicked.connect(on_button_click)
        button2.clicked.connect(on_button_click)
        button3.clicked.connect(on_button_click)
        button4.clicked.connect(on_button_click)

        # Show the menu window
        promMenu.exec_()
        # Start the application event loop

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
        self.view.setScene(ChessBoard(self.boardSet, self.variant, self, self.GS))


# Initialize the App
if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = UI('s')
    app.exec_()
