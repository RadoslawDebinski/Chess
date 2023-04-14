import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton, QLineEdit, QGridLayout, QMainWindow, QComboBox
from PyQt5 import uic


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the ui file
        uic.loadUi("startui.ui", self)
        self.setWindowTitle("Input")

        # Define Our Widgets
        self.lineEdit = self.findChild(QLineEdit, "lineEdit")
        self.singleButton = self.findChild(QRadioButton, "radioButton")
        self.multiButton = self.findChild(QRadioButton, "radioButton_2")
        self.loadSqlite = self.findChild(QComboBox, "comboBox")
        self.loadXML = self.findChild(QComboBox, "comboBox_2")
        self.loadSetting = self.findChild(QComboBox, "comboBox_3")
        # Set up mask
        self.lineEdit.setInputMask('000.000.000.000:00000')

        # Show the app
        self.show()


# Initialize the App
if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()
