import sys
from PyQt6.QtGui import QPainter, QPen, QBrush
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget


class KeyViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Key Viewer')
        self.setFixedSize(320, 180)

        self.key_up = False
        self.key_down = False
        self.key_left = False
        self.key_right = False
        self.key_a = False
        self.key_b = False

        self.qtimer = QTimer(self)
        self.qtimer.timeout.connect(self.timer)
        self.qtimer.start(1000 // 60)

    def timer(self):
        self.update()

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)

        painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
        painter.setBrush(QBrush(Qt.GlobalColor.red if self.key_a else Qt.GlobalColor.white))
        painter.drawRect(30, 40, 40, 40)
        painter.setPen(QPen(Qt.GlobalColor.white if self.key_a else Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
        painter.drawText(30 + 16, 40 + 24, 'A')

        painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
        painter.setBrush(QBrush(Qt.GlobalColor.red if self.key_b else Qt.GlobalColor.white))
        painter.drawRect(80, 90, 40, 40)
        painter.setPen(QPen(Qt.GlobalColor.white if self.key_b else Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
        painter.drawText(80 + 16, 90 + 24, 'B')

        painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
        painter.setBrush(QBrush(Qt.GlobalColor.red if self.key_up else Qt.GlobalColor.white))
        painter.drawRect(200, 40, 40, 40)
        painter.setPen(QPen(Qt.GlobalColor.white if self.key_up else Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
        painter.drawText(200 + 14, 40 + 24, '↑')

        painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
        painter.setBrush(QBrush(Qt.GlobalColor.red if self.key_down else Qt.GlobalColor.white))
        painter.drawRect(200, 90, 40, 40)
        painter.setPen(QPen(Qt.GlobalColor.white if self.key_down else Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
        painter.drawText(200 + 14, 90 + 24, '↓')

        painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
        painter.setBrush(QBrush(Qt.GlobalColor.red if self.key_left else Qt.GlobalColor.white))
        painter.drawRect(150, 90, 40, 40)
        painter.setPen(QPen(Qt.GlobalColor.white if self.key_left else Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
        painter.drawText(150 + 14, 90 + 24, '←')

        painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
        painter.setBrush(QBrush(Qt.GlobalColor.red if self.key_right else Qt.GlobalColor.white))
        painter.drawRect(250, 90, 40, 40)
        painter.setPen(QPen(Qt.GlobalColor.white if self.key_right else Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
        painter.drawText(250 + 14, 90 + 24, '→')

        painter.end()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Up:
            self.key_up = True
        if key == Qt.Key.Key_Down:
            self.key_down = True
        if key == Qt.Key.Key_Left:
            self.key_left = True
        if key == Qt.Key.Key_Right:
            self.key_right = True
        if key == Qt.Key.Key_A:
            self.key_a = True
        if key == Qt.Key.Key_B:
            self.key_b = True

    def keyReleaseEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Up:
            self.key_up = False
        if key == Qt.Key.Key_Down:
            self.key_down = False
        if key == Qt.Key.Key_Left:
            self.key_left = False
        if key == Qt.Key.Key_Right:
            self.key_right = False
        if key == Qt.Key.Key_A:
            self.key_a = False
        if key == Qt.Key.Key_B:
            self.key_b = False


def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    print(traceback.format_exc())
    exit(1)


if __name__ == '__main__':
    sys.excepthook = exception_hook
    qapp = QApplication(sys.argv)
    key_viewer = KeyViewer()
    key_viewer.show()
    sys.exit(qapp.exec())
