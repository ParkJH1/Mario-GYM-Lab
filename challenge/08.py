import os.path

from PyQt6.QtGui import QImage, QPixmap, QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QComboBox
import sys
import retro
import numpy as np
import random


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


def relu(x):
    return np.maximum(0, x)


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.maximum(-700, x)))


class Chromosome:
    def __init__(self):
        self.w1 = np.random.uniform(low=-1, high=1, size=(10 * 8, 11))
        self.b1 = np.random.uniform(low=-1, high=1, size=(11,))

        self.w2 = np.random.uniform(low=-1, high=1, size=(11, 6))
        self.b2 = np.random.uniform(low=-1, high=1, size=(6,))

        self.distance = 0
        self.max_distance = 0
        self.frames = 0
        self.stop_frames = 0
        self.win = 0

    def predict(self, data):
        layer1 = relu(np.matmul(data, self.w1) + self.b1)
        output = sigmoid(np.matmul(layer1, self.w2) + self.b2)
        result = (output > 0.5).astype(np.int)
        return result

    def fitness(self):
        # 적합도(점수) 기준
        # 1. 많은 거리를 이동할수록 높은 점수
        # 2. 같은 거리를 더 짧은 시간에 도달할수록 점수
        # 3. 조금이라도 앞으로 이동했다면 기본 점수(2500) 획득
        # 4. 클리어한 경우 매우 높은 점수(1000000) 획득
        # 5. 아무리 낮아도 최저 점수(1) 보장
        return int(max(self.distance ** 1.8 - self.frames ** 1.5 + min(max(self.distance - 50, 0), 1) * 2500 + self.win * 1000000, 1))


class GeneticAlgorithm:
    def __init__(self):
        self.generation = 0
        self.generation_size = 10
        self.chromosomes = []

        for i in range(self.generation_size):
            chromosome = Chromosome()
            self.chromosomes.append(chromosome)

    def selection(self):
        return self.roulette_wheel_selection()

    def roulette_wheel_selection(self):
        result = []
        fitness_sum = sum(c.fitness() for c in self.chromosomes)
        for _ in range(2):
            pick = random.uniform(0, fitness_sum)
            current = 0
            for chromosome in self.chromosomes:
                current += chromosome.fitness()
                if current > pick:
                    result.append(chromosome)
                    break
        return result

    def crossover(self, chromosome1, chromosome2):
        child1 = Chromosome()
        child2 = Chromosome()

        child1.w1, child2.w1 = self.simulated_binary_crossover(chromosome1.w1, chromosome2.w1)
        child1.b1, child2.b1 = self.simulated_binary_crossover(chromosome1.b1, chromosome2.b1)
        child1.w2, child2.w2 = self.simulated_binary_crossover(chromosome1.w2, chromosome2.w2)
        child1.b2, child2.b2 = self.simulated_binary_crossover(chromosome1.b2, chromosome2.b2)

        return child1, child2

    def simulated_binary_crossover(self, p1, p2):
        rand = np.random.random(p1.shape)
        gamma = np.empty(p1.shape)
        gamma[rand <= 0.5] = (2 * rand[rand <= 0.5]) ** (1.0 / (100 + 1))
        gamma[rand > 0.5] = (1.0 / (2.0 * (1.0 - rand[rand > 0.5]))) ** (1.0 / (100 + 1))
        c1 = 0.5 * ((1 + gamma) * p1 + (1 - gamma) * p2)
        c2 = 0.5 * ((1 - gamma) * p1 + (1 + gamma) * p2)
        return c1, c2

    def mutation(self, chromosome):
        self.static_mutation(chromosome.w1)
        self.static_mutation(chromosome.b1)
        self.static_mutation(chromosome.w2)
        self.static_mutation(chromosome.b2)

    def static_mutation(self, data):
        mutation_array = np.random.random(data.shape) < 0.05
        gaussian_mutation = np.random.normal(size=data.shape)
        data[mutation_array] += gaussian_mutation[mutation_array]

    def elitist_preserve(self):
        sort_chromosomes = sorted(self.chromosomes, key=lambda x: x.fitness(), reverse=True)
        return sort_chromosomes[:int(self.generation_size * 0.1)]

    def next_generation(self):
        next_chromosomes = []
        next_chromosomes.extend(self.elitist_preserve())

        np.save('../model/my_model/w1.npy', next_chromosomes[0].w1)
        np.save('../model/my_model/b1.npy', next_chromosomes[0].b1)
        np.save('../model/my_model/w2.npy', next_chromosomes[0].w2)
        np.save('../model/my_model/b2.npy', next_chromosomes[0].b2)

        while len(next_chromosomes) < self.generation_size:
            selected_chromosome = self.selection()

            child_chromosome1, child_chromosome2 = self.crossover(selected_chromosome[0], selected_chromosome[1])
            self.mutation(child_chromosome1)
            self.mutation(child_chromosome2)

            next_chromosomes.append(child_chromosome1)
            if len(next_chromosomes) == self.generation_size:
                break
            next_chromosomes.append(child_chromosome2)

        self.chromosomes = next_chromosomes
        self.generation += 1


class MarioAI(QWidget):
    def __init__(self, main, level, speed, replay):
        super().__init__()
        self.setWindowTitle('Mario AI')
        self.main = main

        self.replay = replay

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

        self.press_buttons = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])

        self.screen_label = QLabel(self)
        self.screen_label.setGeometry(0, 0, self.screen_width, self.screen_height)

        self.update_screen()

        if self.replay:
            self.chromosome = Chromosome()
            if os.path.exists('../model/my_model/w1.npy'):
                self.chromosome.w1 = np.load('../model/my_model/w1.npy')
            if os.path.exists('../model/my_model/b1.npy'):
                self.chromosome.b1 = np.load('../model/my_model/b1.npy')
            if os.path.exists('../model/my_model/w2.npy'):
                self.chromosome.w2 = np.load('../model/my_model/w2.npy')
            if os.path.exists('../model/my_model/b2.npy'):
                self.chromosome.b2 = np.load('../model/my_model/b2.npy')
        else:
            self.ga = GeneticAlgorithm()
            self.current_chromosome_index = 0
            print('==== 0 세대 ====')

        self.qtimer = QTimer(self)
        self.qtimer.timeout.connect(self.timer)
        if speed == 0:
            self.qtimer.start(1000 // 30)
        elif speed == 1:
            self.qtimer.start(1000 // 60)
        else:
            self.qtimer.start(1000 // 144)

    def timer(self):
        self.update_screen()
        self.update()

    def update_screen(self):
        self.screen_image = self.env.get_screen()

        self.screen_qimage = QImage(self.screen_image, self.screen_image.shape[1], self.screen_image.shape[0],
                                    QImage.Format.Format_RGB888)
        self.screen_pixmap = QPixmap(self.screen_qimage)
        self.screen_pixmap = self.screen_pixmap.scaled(self.screen_width, self.screen_height,
                                                       Qt.AspectRatioMode.IgnoreAspectRatio)

        self.screen_label.setPixmap(self.screen_pixmap)

    def paintEvent(self, event):
        ram = self.env.get_ram()

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

        for i in range(screen_tiles.shape[0]):
            for j in range(screen_tiles.shape[1]):
                if screen_tiles[i][j] > 0:
                    screen_tiles[i][j] = 1
                if screen_tiles[i][j] == -1:
                    screen_tiles[i][j] = 2

        player_x_position_current_screen_offset = ram[0x03AD]
        player_y_position_current_screen_offset = ram[0x03B8]
        px = (player_x_position_current_screen_offset + 8) // 16
        py = (player_y_position_current_screen_offset + 8) // 16 - 1

        ix = px
        if ix + 8 > screen_tiles.shape[1]:
            ix = screen_tiles.shape[1] - 8
        iy = 2

        input_data = screen_tiles[iy:iy + 10, ix:ix + 8]

        if 2 <= py <= 11:
            input_data[py - 2][0] = 2

        input_data = input_data.flatten()

        if self.replay:
            self.chromosome.frames += 1
            self.chromosome.distance = ram[0x006D] * 256 + ram[0x0086]

            if self.chromosome.max_distance < self.chromosome.distance:
                self.chromosome.max_distance = self.chromosome.distance
                self.chromosome.stop_frame = 0
            else:
                self.chromosome.stop_frame += 1

            if ram[0x001D] == 3 or ram[0x0E] in (0x0B, 0x06) or ram[0xB5] == 2 or self.chromosome.stop_frame > 180:
                if ram[0x001D] == 3:
                    self.chromosome.win = 1

                self.current_fitness = self.chromosome.fitness()
                print(f'적합도: {self.current_fitness}')

                self.chromosome.win = 0
                self.chromosome.frames = 0
                self.chromosome.distance = 0
                self.chromosome.max_distance = 0
                self.chromosome.stop_frames = 0

                self.env.reset()
            else:
                self.predict = self.chromosome.predict(input_data)

                self.key_up = self.predict[0] == 1
                self.key_down = self.predict[1] == 1
                self.key_left = self.predict[2] == 1
                self.key_right = self.predict[3] == 1
                self.key_a = self.predict[4] == 1
                self.key_b = self.predict[5] == 1

                self.press_buttons = np.array(
                    [self.predict[5], 0, 0, 0, self.predict[0], self.predict[1], self.predict[2], self.predict[3],
                     self.predict[4]])
                self.env.step(self.press_buttons)
        else:
            current_chromosome = self.ga.chromosomes[self.current_chromosome_index]
            current_chromosome.frames += 1
            current_chromosome.distance = ram[0x006D] * 256 + ram[0x0086]

            if current_chromosome.max_distance < current_chromosome.distance:
                current_chromosome.max_distance = current_chromosome.distance
                current_chromosome.stop_frame = 0
            else:
                current_chromosome.stop_frame += 1

            if ram[0x001D] == 3 or ram[0x0E] in (0x0B, 0x06) or ram[0xB5] == 2 or current_chromosome.stop_frame > 180:
                if ram[0x001D] == 3:
                    current_chromosome.win = 1

                self.current_fitness = current_chromosome.fitness()
                print(f'{self.current_chromosome_index + 1}번 마리오: {self.current_fitness}')

                self.current_chromosome_index += 1

                if self.current_chromosome_index == self.ga.generation_size:
                    self.current_chromosome_index = 0
                    print(f'엘리트 적합도: {max([chromosome.fitness() for chromosome in self.ga.chromosomes])}')
                    self.ga.next_generation()
                    print(f'==== {self.ga.generation} 세대 ====')

                self.env.reset()
            else:
                self.predict = current_chromosome.predict(input_data)

                self.key_up = self.predict[0] == 1
                self.key_down = self.predict[1] == 1
                self.key_left = self.predict[2] == 1
                self.key_right = self.predict[3] == 1
                self.key_a = self.predict[4] == 1
                self.key_b = self.predict[5] == 1

                self.press_buttons = np.array(
                    [self.predict[5], 0, 0, 0, self.predict[0], self.predict[1], self.predict[2], self.predict[3],
                     self.predict[4]])
                self.env.step(self.press_buttons)

        self.main.mario_tile_map.update()
        self.main.mario_key_viewer.update()


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
        self.mario_ai_button.clicked.connect(self.run_mario_ai)

        self.mario_replay_button = QPushButton(self)
        self.mario_replay_button.setText('Replay')
        self.mario_replay_button.setGeometry(120, 120, 120, 40)
        self.mario_replay_button.clicked.connect(self.run_mario_replay)

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
        self.mario_tile_map = MarioTileMap(self)
        self.mario_tile_map.show()
        self.mario_key_viewer = MarioKeyViewer(self)
        self.mario_key_viewer.show()
        self.mario = Mario(self, self.game_level_combo_box.currentIndex(), self.game_speed_combo_box.currentIndex())
        self.mario.show()
        self.hide()

    def run_mario_ai(self):
        self.mario_tile_map = MarioTileMap(self)
        self.mario_tile_map.show()
        self.mario_key_viewer = MarioKeyViewer(self)
        self.mario_key_viewer.show()
        self.mario = MarioAI(self, self.game_level_combo_box.currentIndex(), self.game_speed_combo_box.currentIndex(), False)
        self.mario.show()
        self.hide()

    def run_mario_replay(self):
        self.mario_tile_map = MarioTileMap(self)
        self.mario_tile_map.show()
        self.mario_key_viewer = MarioKeyViewer(self)
        self.mario_key_viewer.show()
        self.mario = MarioAI(self, self.game_level_combo_box.currentIndex(), self.game_speed_combo_box.currentIndex(), True)
        self.mario.show()
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
