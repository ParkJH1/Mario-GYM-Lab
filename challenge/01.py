from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
import sys


class MarioGYM(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mario GYM')
        self.setFixedSize(360, 240)

        self.mario_button = QPushButton(self)
        self.mario_button.setText('Super Mario Bros.')
        self.mario_button.setGeometry(120, 50, 120, 40)

        self.mario_ai_button = QPushButton(self)
        self.mario_ai_button.setText('Mario GYM')
        self.mario_ai_button.setGeometry(120, 100, 120, 40)

        self.mario_replay_button = QPushButton(self)
        self.mario_replay_button.setText('Replay')
        self.mario_replay_button.setGeometry(120, 150, 120, 40)


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
