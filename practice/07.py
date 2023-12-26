import sys
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget


class MarioAINetwork(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Neural Network')

        self.setFixedSize(480, 480)

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)

        for i in range(5):
            painter.setPen(QPen(Qt.GlobalColor.red if i % 2 == 0 else Qt.GlobalColor.blue, 2, Qt.PenStyle.SolidLine))
            painter.drawLine(240 - 40 * (5 - i), 0, 240 - 40 * (5 - i), 240 - 100)
            painter.setPen(QPen(Qt.GlobalColor.red if i % 2 == 0 else Qt.GlobalColor.blue, 2, Qt.PenStyle.SolidLine))
            painter.drawLine(240 + 40 * (5 - i), 0, 240 + 40 * (5 - i), 240 - 100)
        painter.setPen(QPen(Qt.GlobalColor.red, 2, Qt.PenStyle.SolidLine))
        painter.drawLine(240, 0, 240, 240 - 100)

        for i in range(5):
            for j in range(3):
                painter.setPen(QPen(Qt.GlobalColor.red if j % 2 == 0 else Qt.GlobalColor.blue, 2, Qt.PenStyle.SolidLine))
                painter.drawLine(240 - 40 * (5 - i), 240 - 100, 240 - 30 - 60 * (2 - j), 240 + 100)
                painter.setPen(QPen(Qt.GlobalColor.red if j % 2 == 0 else Qt.GlobalColor.blue, 2, Qt.PenStyle.SolidLine))
                painter.drawLine(240 + 40 * (5 - i), 240 - 100, 240 - 30 - 60 * (2 - j), 240 + 100)
                painter.setPen(QPen(Qt.GlobalColor.red if j % 2 == 0 else Qt.GlobalColor.blue, 2, Qt.PenStyle.SolidLine))
                painter.drawLine(240 - 40 * (5 - i), 240 - 100, 240 - 30 + 60 * (2 - j), 240 + 100)
                painter.setPen(QPen(Qt.GlobalColor.red if j % 2 == 0 else Qt.GlobalColor.blue, 2, Qt.PenStyle.SolidLine))
                painter.drawLine(240 + 40 * (5 - i), 240 - 100, 240 + 30 + 60 * (2 - j), 240 + 100)

        for j in range(3):
            painter.setPen(QPen(Qt.GlobalColor.red if j % 2 == 0 else Qt.GlobalColor.blue, 2, Qt.PenStyle.SolidLine))
            painter.drawLine(240, 240 - 100, 240 - 30 - 60 * (2 - j), 240 + 100)
            painter.setPen(QPen(Qt.GlobalColor.red if j % 2 == 0 else Qt.GlobalColor.blue, 2, Qt.PenStyle.SolidLine))
            painter.drawLine(240, 240 - 100, 240 + 30 + 60 * (2 - j), 240 + 100)

        painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))

        for i in range(5):
            painter.setBrush(QBrush(QColor.fromHslF(125 / 239, 0 if i % 2 == 0 else 1, 120 / 240)))
            painter.drawEllipse(240 - 16 - 40 * (5 - i), 240 - 16 - 100, 16 * 2, 16 * 2)
            painter.setBrush(QBrush(QColor.fromHslF(125 / 239, 0 if i % 2 == 0 else 1, 120 / 240)))
            painter.drawEllipse(240 - 16 + 40 * (5 - i), 240 - 16 - 100, 16 * 2, 16 * 2)
        painter.setBrush(QBrush(QColor.fromHslF(125 / 239, 1, 120 / 240)))
        painter.drawEllipse(240 - 16, 240 - 16 - 100, 16 * 2, 16 * 2)

        for i in range(3):
            painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
            painter.setBrush(QBrush(QColor.fromHslF(0.8, 0 if i % 2 == 0 else 1, 0.8)))
            painter.drawEllipse(240 - 16 - 30 - 60 * (2 - i), 240 - 16 + 100, 16 * 2, 16 * 2)
            painter.setBrush(QBrush(QColor.fromHslF(0.8, 0 if i % 2 == 0 else 1, 0.8)))
            painter.drawEllipse(240 - 16 + 30 + 60 * (2 - i), 240 - 16 + 100, 16 * 2, 16 * 2)

            painter.drawText(240 - 16 - 30 - 60 * (2 - i) + 12, 240 - 16 + 100 + 19, ('U', 'D', 'L', 'R', 'A', 'B')[i])
            painter.drawText(240 - 16 + 30 + 60 * (2 - i) + 12, 240 - 16 + 100 + 19, ('U', 'D', 'L', 'R', 'A', 'B')[6 - 1 - i])

        painter.end()


def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    print(traceback.format_exc())
    exit(1)


if __name__ == '__main__':
    sys.excepthook = exception_hook
    qapp = QApplication(sys.argv)
    network = MarioAINetwork()
    network.show()
    sys.exit(qapp.exec())
