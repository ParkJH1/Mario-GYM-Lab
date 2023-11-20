from PyQt6.QtGui import QImage, QPixmap, QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QComboBox
import sys
import retro
import numpy as np


class Mario(QWidget):
    def __init__(self, main, level, speed):
        super().__init__()
        self.main = main
        self.setWindowTitle('Mario')

        self.env = retro.make(game='SuperMarioBros-Nes', state=f'Level{level + 1}-1')
        self.screen_image = self.env.reset()
        self.screen_width = self.screen_image.shape[0] * 2
        self.screen_height = self.screen_image.shape[0] * 2

        self.setFixedSize(self.screen_width, self.screen_height)
        self.move(100, 100)

        self.key_up = False
        self.key_down = False
        self.key_left = False
        self.key_right = False
        self.key_a = False
        self.key_b = False

        self.screen_label = QLabel(self)
        self.screen_label.setGeometry(0, 0, self.screen_width, self.screen_height)

        self.update_screen()

        self.qtimer = QTimer(self)
        self.qtimer.timeout.connect(self.timer)
        if speed == 0:
            self.qtimer.start(1000 // 30)
        elif speed == 1:
            self.qtimer.start(1000 // 60)
        else:
            self.qtimer.start(1000 // 144)

    def timer(self):
        self.env.step(np.array([self.key_b, 0, 0, 0, self.key_up, self.key_down, self.key_left, self.key_right, self.key_a]))
        self.update_screen()
        self.update()

    def update_screen(self):
        self.screen_image = self.env.get_screen()

        self.screen_qimage = QImage(self.screen_image, self.screen_image.shape[1], self.screen_image.shape[0], QImage.Format.Format_RGB888)
        self.screen_pixmap = QPixmap(self.screen_qimage)
        self.screen_pixmap = self.screen_pixmap.scaled(self.screen_width, self.screen_height, Qt.AspectRatioMode.IgnoreAspectRatio)

        self.screen_label.setPixmap(self.screen_pixmap)

    def paintEvent(self, event):
        self.main.mario_tile_map.update()
        self.main.mario_key_viewer.update()

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


class MarioTileMap(QWidget):
    def __init__(self, main):
        super().__init__()
        self.setWindowTitle('Tile Map')
        self.main = main

        self.setFixedSize(16 * 20, 13 * 20)
        self.move(560, 100)

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)

        ram = self.main.mario.env.get_ram()

        full_screen_tiles = ram[0x0500:0x069F + 1]
        full_screen_tile_count = full_screen_tiles.shape[0]

        full_screen_page1_tiles = full_screen_tiles[:full_screen_tile_count // 2].reshape((-1, 16))
        full_screen_page2_tiles = full_screen_tiles[full_screen_tile_count // 2:].reshape((-1, 16))

        full_screen_tiles = np.concatenate((full_screen_page1_tiles, full_screen_page2_tiles), axis=1).astype(np.int)

        enemy_drawn = ram[0x000F:0x0014]
        enemy_horizontal_position_in_level = ram[0x006E:0x0072 + 1]
        enemy_x_position_on_screen = ram[0x0087:0x008B + 1]
        enemy_y_position_on_screen = ram[0x00CF:0x00D3 + 1]

        for i in range(5):
            if enemy_drawn[i] == 1:
                ex = (((enemy_horizontal_position_in_level[i] * 256) + enemy_x_position_on_screen[i]) % 512 + 8) // 16
                ey = (enemy_y_position_on_screen[i] - 8) // 16 - 1
                if 0 <= ex < full_screen_tiles.shape[1] and 0 <= ey < full_screen_tiles.shape[0]:
                    full_screen_tiles[ey][ex] = -1

        current_screen_in_level = ram[0x071A]
        screen_x_position_in_level = ram[0x071C]
        screen_x_position_offset = (256 * current_screen_in_level + screen_x_position_in_level) % 512
        sx = screen_x_position_offset // 16

        screen_tiles = np.concatenate((full_screen_tiles, full_screen_tiles), axis=1)[:, sx:sx + 16]

        painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
        for i in range(screen_tiles.shape[0]):
            for j in range(screen_tiles.shape[1]):
                if screen_tiles[i][j] > 0:
                    screen_tiles[i][j] = 1
                if screen_tiles[i][j] == -1:
                    screen_tiles[i][j] = 2
                    painter.setBrush(QBrush(Qt.GlobalColor.red))
                else:
                    painter.setBrush(QBrush(QColor.fromHslF(125 / 239, 0 if screen_tiles[i][j] == 0 else 1, 120 / 240)))
                painter.drawRect(20 * j, 20 * i, 20, 20)

        player_x_position_current_screen_offset = ram[0x03AD]
        player_y_position_current_screen_offset = ram[0x03B8]
        px = (player_x_position_current_screen_offset + 8) // 16
        py = (player_y_position_current_screen_offset + 8) // 16 - 1
        painter.setBrush(QBrush(Qt.GlobalColor.blue))
        painter.drawRect(20 * px, 20 * py, 20, 20)

        painter.end()


class MarioKeyViewer(QWidget):
    def __init__(self, main):
        super().__init__()
        self.setWindowTitle('Key Viewer')
        self.main = main

        self.setFixedSize(320, 180)
        self.move(560, 400)

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)

        try:
            painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
            painter.setBrush(QBrush(Qt.GlobalColor.red if self.main.mario.key_a else Qt.GlobalColor.white))
            painter.drawRect(30, 40, 40, 40)
            painter.setPen(QPen(Qt.GlobalColor.white if self.main.mario.key_a else Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
            painter.drawText(30 + 16, 40 + 24, 'A')

            painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
            painter.setBrush(QBrush(Qt.GlobalColor.red if self.main.mario.key_b else Qt.GlobalColor.white))
            painter.drawRect(80, 90, 40, 40)
            painter.setPen(QPen(Qt.GlobalColor.white if self.main.mario.key_b else Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
            painter.drawText(80 + 16, 90 + 24, 'B')

            painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
            painter.setBrush(QBrush(Qt.GlobalColor.red if self.main.mario.key_up else Qt.GlobalColor.white))
            painter.drawRect(200, 40, 40, 40)
            painter.setPen(QPen(Qt.GlobalColor.white if self.main.mario.key_up else Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
            painter.drawText(200 + 14, 40 + 24, '↑')

            painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
            painter.setBrush(QBrush(Qt.GlobalColor.red if self.main.mario.key_down else Qt.GlobalColor.white))
            painter.drawRect(200, 90, 40, 40)
            painter.setPen(QPen(Qt.GlobalColor.white if self.main.mario.key_down else Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
            painter.drawText(200 + 14, 90 + 24, '↓')

            painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
            painter.setBrush(QBrush(Qt.GlobalColor.red if self.main.mario.key_left else Qt.GlobalColor.white))
            painter.drawRect(150, 90, 40, 40)
            painter.setPen(QPen(Qt.GlobalColor.white if self.main.mario.key_left else Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
            painter.drawText(150 + 14, 90 + 24, '←')

            painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
            painter.setBrush(QBrush(Qt.GlobalColor.red if self.main.mario.key_right else Qt.GlobalColor.white))
            painter.drawRect(250, 90, 40, 40)
            painter.setPen(QPen(Qt.GlobalColor.white if self.main.mario.key_right else Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
            painter.drawText(250 + 14, 90 + 24, '→')
        except:
            pass

        painter.end()


class MarioGYM(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mario GYM')
        self.setFixedSize(360, 240)

        self.mario_button = QPushButton(self)
        self.mario_button.setText('Super Mario Bros.')
        self.mario_button.setGeometry(120, 20, 120, 40)
        self.mario_button.clicked.connect(self.run_mario)

        self.mario_ai_button = QPushButton(self)
        self.mario_ai_button.setText('Mario GYM')
        self.mario_ai_button.setGeometry(120, 70, 120, 40)

        self.mario_replay_button = QPushButton(self)
        self.mario_replay_button.setText('Replay')
        self.mario_replay_button.setGeometry(120, 120, 120, 40)

        self.game_level_combo_box = QComboBox(self)
        self.game_level_combo_box.addItem('Level 1')
        self.game_level_combo_box.addItem('Level 2')
        self.game_level_combo_box.addItem('Level 3')
        self.game_level_combo_box.addItem('Level 4')
        self.game_level_combo_box.addItem('Level 5')
        self.game_level_combo_box.addItem('Level 6')
        self.game_level_combo_box.addItem('Level 7')
        self.game_level_combo_box.addItem('Level 8')
        self.game_level_combo_box.setGeometry(120, 170, 120, 20)

        self.game_speed_combo_box = QComboBox(self)
        self.game_speed_combo_box.addItem('보통 속도')
        self.game_speed_combo_box.addItem('빠른 속도')
        self.game_speed_combo_box.addItem('최고 속도')
        self.game_speed_combo_box.setGeometry(120, 200, 120, 20)

    def run_mario(self):
        self.mario = Mario(self, self.game_level_combo_box.currentIndex(), self.game_speed_combo_box.currentIndex())
        self.mario.show()
        self.mario_tile_map = MarioTileMap(self)
        self.mario_tile_map.show()
        self.mario_key_viewer = MarioKeyViewer(self)
        self.mario_key_viewer.show()
        self.hide()


def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    print(traceback.format_exc())
    exit(1)


if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    mario_gym = MarioGYM()
    mario_gym.show()
    sys.exit(app.exec())
