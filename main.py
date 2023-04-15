import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton, QLineEdit, QGridLayout, QMainWindow, QComboBox, \
    QPushButton
from PyQt5 import uic
from loadGame import UI
import json


class InputUI(QMainWindow):
    def __init__(self):
        super(InputUI, self).__init__()

        # Load the ui file
        uic.loadUi("startui.ui", self)
        self.setWindowTitle("Input")

        # Define Our Widgets
        self.lineEdit = self.findChild(QLineEdit, "lineEdit")
        self.singleButton = self.findChild(QRadioButton, "radioButton")
        self.multiButton = self.findChild(QRadioButton, "radioButton_2")
        self.aiButton = self.findChild(QRadioButton, "radioButton_3")
        self.loadHistory = self.findChild(QComboBox, "comboBox")
        self.loadConfig = self.findChild(QComboBox, "comboBox_3")
        self.applyButton = self.findChild(QPushButton, "pushButton")
        # Set up mask
        self.lineEdit.setInputMask('000.000.000.000:00000;_')
        # Set up choices for history
        folderPath = 'saves'
        fileNames = [f for f in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, f))]
        self.loadHistory.addItem(None)
        [self.loadHistory.addItem(file_name) for file_name in fileNames]
        # Set up choices for settings
        folderPath = 'configs'
        fileNames = [f for f in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, f))]
        self.loadConfig.addItem(None)
        [self.loadConfig.addItem(file_name) for file_name in fileNames]
        # Connect Apply button to start function
        self.applyButton.clicked.connect(self.startGame)
        # Show the app
        self.show()

    def startGame(self):
        # Hide current Input UI
        self.hide()
        # Get dirs from Input UI
        historySource = self.loadHistory.currentText()
        configSource = self.loadConfig.currentText()
        # Get config from source
        if configSource != '':
            with open(f'configs\\{configSource}', 'r') as file:
                conf = json.load(file)
        else:
            conf = 's'

        UI(conf, historySource)


# Initialize the App
if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = InputUI()
    app.exec_()
