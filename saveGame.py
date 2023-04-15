import numpy as np
from datetime import datetime
import sqlite3
import xml.etree.ElementTree as ET
import json


class SaveGame:
    def __init__(self, GS, variant):
        self.GS = GS
        self.variant = variant
        # Create file name from current date
        now = datetime.now()  # get the current date and time
        formatted_date = now.strftime("%Y-%m-%d-%H-%M-%S")  # format the date and time as a string
        self.filename = f"save_{formatted_date}"  # use the formatted date string as part of the file name
        self.createSqlite3()
        self.createXML()
        self.createJson()

    def createSqlite3(self):
        # Connect to database
        conn = sqlite3.connect(f'saves\\{self.filename}.db')

        # Create table
        c = conn.cursor()
        c.execute('CREATE TABLE myTable (fromRow INTEGER, fromCol INTEGER, toRow INTEGER, toCol INTEGER)')

        # Insert data
        [self.insertInto(c, i) for i in range(len(self.GS.stackFrom))]

        # Save changes and close connection
        conn.commit()
        conn.close()

    def insertInto(self, c, i):
        row = self.GS.stackFrom[i] + self.GS.stackTo[i]
        c.execute('INSERT INTO myTable (fromRow, fromCol, toRow, toCol) VALUES (?, ?, ?, ?)', row)

    def createXML(self):
        # Create root element
        root = ET.Element('lists')

        # Create elements for list1
        list1_elem = ET.SubElement(root, 'movesFrom')
        for sublist in self.GS.stackFrom:
            sublist_elem = ET.SubElement(list1_elem, 'move')
            for item in sublist:
                item_elem = ET.SubElement(sublist_elem, 'position')
                item_elem.text = str(item)

        # Create elements for list2
        list2_elem = ET.SubElement(root, 'movesTo')
        for sublist in self.GS.stackTo:
            sublist_elem = ET.SubElement(list2_elem, 'move')
            for item in sublist:
                item_elem = ET.SubElement(sublist_elem, 'position')
                item_elem.text = str(item)

        # Create XML tree and write to file
        tree = ET.ElementTree(root)
        tree.write(f'saves\\{self.filename}.xml')

    def createJson(self):
        with open(f'configs\\{self.filename}.json', 'w') as file:
            json.dump(self.variant, file)



