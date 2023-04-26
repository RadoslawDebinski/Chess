from math import sin, pi, cos

from PyQt5.QtCore import Qt, QTimer, QTime, QRectF, QLineF, QPointF
from PyQt5.QtGui import QColor, QBrush, QPainter, QPen
from PyQt5.QtWidgets import QGraphicsEllipseItem


class ChessClock(QGraphicsEllipseItem):

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update1)
        self.elapsed_time = QTime(11, 50, 0)  # initial elapsed time
        self.setRect(0, 0, 200, 200)  # set the size of the clock

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)  # smooth edges
        painter.setPen(QPen(Qt.black, 2))  # black outline
        painter.drawEllipse(self.rect())  # draw the outer circle

        # draw the tick marks for hours
        painter.setPen(QPen(Qt.black, 2))
        center = self.rect().center()
        radius = self.rect().width() / 2
        for i in range(12):
            angle = i * 30
            outer_point = center + QPointF(cos(angle * pi / 180) * radius, sin(angle * pi / 180) * radius)
            inner_point = center + QPointF(cos(angle * pi / 180) * (radius - 15), sin(angle * pi / 180) * (radius - 15))
            painter.drawLine(QLineF(outer_point, inner_point))

        # draw the arrows
        hour_arrow_length = 60
        minute_arrow_length = 90
        second_arrow_length = 90
        millisecond_arrow_length = 100
        hour_angle = (30 * (self.elapsed_time.hour() % 12) +
                      0.5 * self.elapsed_time.minute())
        minute_angle = 6 * self.elapsed_time.minute()
        second_angle = 6 * self.elapsed_time.second()
        millisecond_angle = self.elapsed_time.msec() * 0.36  # 0.36 degrees per millisecond
        hour_arrow = QLineF(center, center + hour_arrow_length *
                            QPointF(sin(hour_angle * pi / 180),
                                    -cos(hour_angle * pi / 180)))  # negative y-coordinates to flip the y-axis
        minute_arrow = QLineF(center, center + minute_arrow_length *
                              QPointF(sin(minute_angle * pi / 180),
                                      -cos(minute_angle * pi / 180)))
        second_arrow = QLineF(center, center + second_arrow_length *
                              QPointF(sin(second_angle * pi / 180),
                                      -cos(second_angle * pi / 180)))
        millisecond_arrow = QLineF(center, center + millisecond_arrow_length *
                              QPointF(sin(millisecond_angle * pi / 180),
                                      -cos(millisecond_angle * pi / 180)))
        painter.setPen(QPen(Qt.black, 3))
        painter.drawLine(hour_arrow)
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(minute_arrow)
        painter.setPen(QPen(Qt.red, 1))
        painter.drawLine(second_arrow)
        painter.setPen(QPen(Qt.blue, 1))
        painter.drawLine(millisecond_arrow)

    def update1(self):
        self.elapsed_time = self.elapsed_time.addMSecs(1)
        self.update()
