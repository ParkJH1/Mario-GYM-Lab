import sys
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 300)
        self.setWindowTitle('MyApp')

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        painter.setPen(QPen(Qt.GlobalColor.blue, 2.0, Qt.PenStyle.SolidLine))
        painter.drawLine(0, 10, 200, 100)

        painter.setPen(QPen(QColor.fromRgb(255, 0, 0), 3.0, Qt.PenStyle.SolidLine))
        painter.setBrush(QBrush(Qt.GlobalColor.blue))
        painter.drawRect(0, 100, 100, 100)

        painter.setPen(QPen(Qt.GlobalColor.black, 1.0, Qt.PenStyle.SolidLine))
        painter.setBrush(QBrush(QColor.fromRgb(0, 255, 0)))
        painter.drawEllipse(100, 100, 100, 100)

        painter.setPen(QPen(Qt.GlobalColor.cyan, 1.0, Qt.PenStyle.SolidLine))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawText(0, 250, 'abcd')

        painter.end()


def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    print(traceback.format_exc())
    exit(1)


if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
