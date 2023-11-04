import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt


class Mario(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 300)
        self.setWindowTitle('Mario')

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Up:
            print('up')
        elif key == Qt.Key.Key_Down:
            print('down')
        elif key == Qt.Key.Key_Left:
            print('left')
        elif key == Qt.Key.Key_Right:
            print('right')
        elif key == Qt.Key.Key_A:
            print('a')
        elif key == Qt.Key.Key_B:
            print('b')

    def keyReleaseEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Up:
            print('up')
        elif key == Qt.Key.Key_Down:
            print('down')
        elif key == Qt.Key.Key_Left:
            print('left')
        elif key == Qt.Key.Key_Right:
            print('right')
        elif key == Qt.Key.Key_A:
            print('a')
        elif key == Qt.Key.Key_B:
            print('b')


def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    print(traceback.format_exc())
    exit(1)


if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    window = Mario()
    window.show()
    sys.exit(app.exec())
