from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QComboBox
import sys


class Mario(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mario')
        self.setFixedSize(400, 400)


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
        self.mario = Mario()
        self.mario.show()


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
