import sys
from PyQt6.QtWidgets import QApplication, QWidget


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 300)
        self.setWindowTitle('MyApp')
        self.show()


def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    print(traceback.format_exc())
    exit(1)


if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec())
