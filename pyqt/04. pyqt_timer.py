import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QTimer


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 300)
        self.setWindowTitle('MyApp')

        self.qtimer = QTimer(self)
        self.qtimer.timeout.connect(self.timer)
        self.qtimer.start(1000)

    def timer(self):
        print('timer')


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
