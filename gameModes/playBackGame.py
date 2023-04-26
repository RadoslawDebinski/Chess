import sqlite3
import xml.etree.ElementTree as ET

import numpy as np

from core.chessEngine import ChessEngine
import time


class Player:
    def __init__(self):
        pass

    def playXML(self, UI, source):
        # Parse XML file
        tree = ET.parse(f'saves\\{source}')
        root = tree.getroot()

        movesFrom = [[int(itemElem.text) for itemElem in sublistElem.findall('position')] for sublistElem in
                     root.find('movesFrom').findall('move')]

        movesTo = [[int(itemElem.text) for itemElem in sublistElem.findall('position')] for sublistElem in
                   root.find('movesTo').findall('move')]

        [self.move(UI, fMove[0], fMove[1], tMove[0], tMove[1]) for fMove, tMove in zip(movesFrom, movesTo)]

    def playDB(self, UI, source):
        # Connect to database
        conn = sqlite3.connect(f'saves\\{source}')

        # Create a cursor
        c = conn.cursor()

        # Execute a SELECT statement to retrieve data from the database
        c.execute('SELECT * FROM myTable')

        # Fetch all the data from the database
        data = c.fetchall()

        [self.move(UI, move[0], move[1], move[2], move[3]) for move in data]

        # Close the connection
        conn.close()

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
