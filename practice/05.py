import sys
from PyQt6.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout, QListWidget, QPushButton, QFormLayout, QLabel, QLineEdit, QComboBox


class MarioAIListTool(QWidget):
    def __init__(self):
        super().__init__()

        self.ai_list_widget = QListWidget()

        self.select_button = QPushButton('선택')

        self.form_layout = QFormLayout()

        self.generation_label = QLabel()
        self.generation_label.setText('1111')
        self.elite_fitness_label = QLabel()
        self.elite_fitness_label.setText('2222')

        self.layer_label = QLabel()
        self.layer_label.setText('3333')
        self.generation_size_label = QLabel()
        self.generation_size_label.setText('4444')
        self.elitist_preserve_rate_label = QLabel()
        self.elitist_preserve_rate_label.setText('5555')
        self.static_mutation_rate_label = QLabel()
        self.static_mutation_rate_label.setText('6666')

        self.form_layout.addRow("학습된 세대: ", self.generation_label)
        self.form_layout.addRow("엘리트 적합도: ", self.elite_fitness_label)
        self.form_layout.addRow("신경망 크기: ", self.layer_label)
        self.form_layout.addRow("세대 크기: ", self.generation_size_label)
        self.form_layout.addRow("엘리트 보존: ", self.elitist_preserve_rate_label)
        self.form_layout.addRow("변이: ", self.static_mutation_rate_label)

        ai_list_layout = QVBoxLayout()
        ai_list_layout.addWidget(self.ai_list_widget)
        ai_list_layout.addWidget(self.select_button)
        ai_list_layout.addLayout(self.form_layout)

        self.setLayout(ai_list_layout)


class MarioAICreateTool(QWidget):
    def __init__(self, toolbox):
        super().__init__()
        self.toolbox = toolbox

        form_layout = QFormLayout()

        self.ai_name_line_edit = QLineEdit()

        self.layer_combo_box = QComboBox()
        self.layer_combo_box.addItem('2')
        self.layer_combo_box.addItem('3')
        self.layer_combo_box.addItem('4')

        self.generation_size_combo_box = QComboBox()
        self.generation_size_combo_box.addItem('10')
        self.generation_size_combo_box.addItem('20')
        self.generation_size_combo_box.addItem('30')
        self.generation_size_combo_box.addItem('40')
        self.generation_size_combo_box.addItem('50')

        self.elitist_preserve_rate_combo_box = QComboBox()
        self.elitist_preserve_rate_combo_box.addItem('0%')
        self.elitist_preserve_rate_combo_box.addItem('10%')
        self.elitist_preserve_rate_combo_box.addItem('20%')
        self.elitist_preserve_rate_combo_box.addItem('30%')
        self.elitist_preserve_rate_combo_box.addItem('40%')
        self.elitist_preserve_rate_combo_box.setCurrentIndex(1)

        self.static_mutation_rate_combo_box = QComboBox()
        self.static_mutation_rate_combo_box.addItem('5%')
        self.static_mutation_rate_combo_box.addItem('10%')
        self.static_mutation_rate_combo_box.addItem('15%')
        self.static_mutation_rate_combo_box.addItem('20%')
        self.static_mutation_rate_combo_box.addItem('25%')

        create_ai_button = QPushButton("생성")
        create_ai_button.clicked.connect(self.create_ai)

        form_layout.addRow("이름: ", self.ai_name_line_edit)
        form_layout.addRow("신경망 크기: ", self.layer_combo_box)
        form_layout.addRow("세대 크기: ", self.generation_size_combo_box)
        form_layout.addRow("엘리트 보존: ", self.elitist_preserve_rate_combo_box)
        form_layout.addRow("변이: ", self.static_mutation_rate_combo_box)
        form_layout.addRow("", create_ai_button)

        self.setLayout(form_layout)

    def create_ai(self):
        self.toolbox.mario_ai_list_tool.ai_list_widget.insertItem(0, self.ai_name_line_edit.text())
        self.toolbox.tabs.setCurrentIndex(0)


class MarioAIToolBox(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AI Tool Box')

        self.setFixedSize(290, 480)

        self.mario_ai_list_tool = MarioAIListTool()
        self.mario_ai_create_tool = MarioAICreateTool(self)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.mario_ai_list_tool, 'AI 목록')
        self.tabs.addTab(self.mario_ai_create_tool, 'AI 생성')

        vbox = QVBoxLayout()
        vbox.addWidget(self.tabs)

        self.setLayout(vbox)


def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    print(traceback.format_exc())
    exit(1)


if __name__ == '__main__':
    sys.excepthook = exception_hook
    qapp = QApplication(sys.argv)
    tool_box = MarioAIToolBox()
    tool_box.show()
    sys.exit(qapp.exec())
