import sqlite3
import xml.etree.ElementTree as ET
from chessEngine import ChessEngine
import time


class Player:
    def __init__(self):
        pass

    def playXML(self, UI, source):
        # Parse XML file
        tree = ET.parse(f'saves\\{source}')
        root = tree.getroot()

        # Extract list data
        list1 = []
        list2 = []

        for sublist_elem in root.find('movesFrom').findall('move'):
            sublist = []
            for item_elem in sublist_elem.findall('position'):
                sublist.append(int(item_elem.text))
            list1.append(sublist)

        for sublist_elem in root.find('movesTo').findall('move'):
            sublist = []
            for item_elem in sublist_elem.findall('position'):
                sublist.append(int(item_elem.text))
            list2.append(sublist)

        [self.move(UI, fMove[0], fMove[1], tMove[0], tMove[1]) for fMove, tMove in zip(list1, list2)]

    def playDB(self, UI, source):
        pass

    def move(self, UI, prevRow, prevCol, newRow, newCol):
        engine = ChessEngine(UI.boardSet, UI.GS)
        UI.boardSet, UI.GS = engine.move(prevRow, prevCol, newRow, newCol)
        # Game stack update
        UI.GS.stackFrom.append([prevRow, prevCol])
        UI.GS.stackTo.append([newRow, newCol])
        UI.GS.changeSide()
        # Report check
        UI.GS.clearStatus()
        UI.GS = engine.checkCheck(UI.boardSet, UI.GS)
        UI.onPieceReleased(UI.boardSet, UI.GS)
        time.sleep(0.25)
