import sys
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
import numpy as np


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 300)
        self.setWindowTitle('GA Mario')

        button = QPushButton(self)
        button.setText('버튼')
        button.setGeometry(100, 100, 50, 50)

        label_text = QLabel(self)
        label_text.setText('가나다')
        label_text.setGeometry(200, 150, 50, 100)

        label_image = QLabel(self)

        image = np.array([[[255, 255, 255], [255, 255, 255]], [[255, 255, 255], [255, 255, 255]]])
        qimage = QImage(image, image.shape[1], image.shape[0], QImage.Format.Format_RGB888)
        pixmap = QPixmap(qimage)
        pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.IgnoreAspectRatio)

        label_image.setPixmap(pixmap)
        label_image.setGeometry(0, 0, 100, 100)


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
