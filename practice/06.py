import sys
from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QFormLayout, QLabel, QHBoxLayout


class MarioAIInfo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Info')

        self.setFixedSize(320, 180)

        self.fitness_list_widget = QListWidget()
        self.fitness_list_widget.setFixedWidth(140)
        self.fitness_list_widget.insertItem(0, 'Mario #1')
        self.fitness_list_widget.insertItem(1, 'Mario #2')
        self.fitness_list_widget.insertItem(2, 'Mario #3')

        self.form_layout = QFormLayout()

        self.generation_label = QLabel()
        self.generation_label.setText('1111')
        self.current_chromosome_index_label = QLabel()
        self.current_chromosome_index_label.setText('2222')
        self.elite_fitness_label = QLabel()
        self.elite_fitness_label.setText('3333')
        self.fitness_label = QLabel()
        self.fitness_label.setText('4444')

        self.form_layout.addRow("현재 세대: ", self.generation_label)
        self.form_layout.addRow("현재 마리오: ", self.current_chromosome_index_label)
        self.form_layout.addRow("엘리트 적합도: ", self.elite_fitness_label)
        self.form_layout.addRow("현재 적합도: ", self.fitness_label)

        ai_list_layout = QHBoxLayout()
        ai_list_layout.addWidget(self.fitness_list_widget)
        ai_list_layout.addLayout(self.form_layout)

        self.setLayout(ai_list_layout)

        self.show()


def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    print(traceback.format_exc())
    exit(1)


if __name__ == '__main__':
    sys.excepthook = exception_hook
    qapp = QApplication(sys.argv)
    info = MarioAIInfo()
    info.show()
    sys.exit(qapp.exec())
