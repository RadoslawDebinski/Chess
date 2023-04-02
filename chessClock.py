from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtWidgets import QGraphicsRectItem


class RotatingBox(QGraphicsRectItem):
    def __init__(self, parent=None):
        super(RotatingBox, self).__init__(parent)
        self.setRect(-50, -50, 100, 100)
        self.setTransformOriginPoint(0, 0)
        self.angle = 0

    def advance(self, phase):
        if phase == 0:
            return
        self.angle += 2
        self.setRotation(self.angle)