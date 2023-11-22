import numpy as np


def relu(x):
    return np.maximum(0, x)


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.maximum(-700, x)))


class Chromosome:
    def __init__(self):
        self.w1 = np.random.uniform(low=-1, high=1, size=(13 * 16, 11))
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
        result = self.chromosomes[:2]
        return result

    def crossover(self, chromosome1, chromosome2):
        child1 = Chromosome()
        child2 = Chromosome()
        return child1, child2

    def mutation(self, chromosome):
        pass

    def next_generation(self):
        next_chromosomes = []
        for i in range(5):
            # 선택
            selected_chromosome = self.selection()

            # 교배
            child_chromosome1, child_chromosome2 = self.crossover(
                selected_chromosome[0],
                selected_chromosome[1]
            )

            # 변이
            self.mutation(child_chromosome1)
            self.mutation(child_chromosome2)

            next_chromosomes.append(child_chromosome1)
            next_chromosomes.append(child_chromosome2)

        self.chromosomes = next_chromosomes
        self.generation += 1


if __name__ == '__main__':
    ga = GeneticAlgorithm()
    print(ga.generation)
    ga.next_generation()
    print(ga.generation)
