import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QBrush, QColor
from PyQt5.QtWidgets import QMenu, QDialog, QVBoxLayout, QPushButton

from core.chessBoard import ChessBoard
import interaction.loadGame


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
    self.piecesBoard = ChessBoard(self.boardSet, self.variant, self, self.GS)
    self.view.setScene(self.piecesBoard)


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
        new_instance = interaction.loadGame.UI(self.variant)
        # Close the current instance
        self.close()
    else:
        self.mateLight.setStyleSheet('QPushButton {background-color: %s}' % QColor(0, 160, 255).name())

    if self.GS.mateKingD:
        self.mateDark.setStyleSheet('QPushButton {background-color: %s}' % QColor(255, 0, 0).name())
        self.mateDark.repaint()
        time.sleep(3)
        # Create a new instance of the UI class
        new_instance = interaction.loadGame.UI(self.variant)
        # Close the current instance
        self.close()
    else:
        self.mateDark.setStyleSheet('QPushButton {background-color: %s}' % QColor(0, 160, 255).name())
    self.mateLight.repaint()
    self.mateDark.repaint()
