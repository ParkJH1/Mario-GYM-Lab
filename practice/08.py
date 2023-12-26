import sys
from PyQt6.QtGui import QPainter, QPen, QBrush
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget
import numpy as np


class MarioAIGraph(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Graph')

        self.setFixedSize(1570, 300)
        self.move(100, 620)

        self.fitness = [1, 2, 3, 4, 5, 6, 7, 8, 10]

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)

        x_len = len(self.fitness)
        y_max = 0

        if x_len >= 1:
            y_max = np.max(self.fitness)

        px = -1
        py = -1

        painter.setPen(QPen(Qt.GlobalColor.blue, 2, Qt.PenStyle.SolidLine))
        for i in range(0, x_len):
            x = int(1560 * (i + 1) / x_len)
            y = int(280 * self.fitness[i] / y_max)

            if px != -1:
                painter.drawLine(px, 290 - py, x, 290 - y)

            px = x
            py = y

        painter.setPen(QPen(Qt.GlobalColor.red, 2, Qt.PenStyle.SolidLine))
        painter.setBrush(QBrush(Qt.GlobalColor.red))

        for i in range(0, x_len):
            x = int(1560 * (i + 1) / x_len)
            y = int(280 * self.fitness[i] / y_max)
            painter.drawEllipse(x - 2, 290 - y - 2, 2 * 2, 2 * 2)

        painter.end()


def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    print(traceback.format_exc())
    exit(1)


if __name__ == '__main__':
    sys.excepthook = exception_hook
    qapp = QApplication(sys.argv)
    graph = MarioAIGraph()
    graph.show()
    sys.exit(qapp.exec())
