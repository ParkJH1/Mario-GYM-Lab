from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget
import sys
import retro


class Mario(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mario')

        self.env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
        self.env.reset()

        self.screen_label = QLabel(self)

        self.screen_image = self.env.get_screen()

        self.screen_width = self.screen_image.shape[0] * 2
        self.screen_height = self.screen_image.shape[0] * 2

        self.setFixedSize(self.screen_width, self.screen_height)

        self.screen_qimage = QImage(self.screen_image, self.screen_image.shape[1], self.screen_image.shape[0], QImage.Format.Format_RGB888)
        self.screen_pixmap = QPixmap(self.screen_qimage)
        self.screen_pixmap = self.screen_pixmap.scaled(self.screen_width, self.screen_height, Qt.AspectRatioMode.IgnoreAspectRatio)

        self.screen_label.setPixmap(self.screen_pixmap)
        self.screen_label.setGeometry(0, 0, self.screen_width, self.screen_height)


def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    print(traceback.format_exc())
    exit(1)


if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    mario = Mario()
    mario.show()
    sys.exit(app.exec())
