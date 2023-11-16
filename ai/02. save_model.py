import numpy as np


def relu(x):
    return np.maximum(0, x)


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


class Model:
    def __init__(self):
        self.w1 = np.random.uniform(low=-1, high=1, size=(13 * 16, 11))
        self.b1 = np.random.uniform(low=-1, high=1, size=(11,))

        self.w2 = np.random.uniform(low=-1, high=1, size=(11, 6))
        self.b2 = np.random.uniform(low=-1, high=1, size=(6,))

    def predict(self, data):
        layer1 = relu(np.matmul(data, self.w1) + self.b1)
        output = sigmoid(np.matmul(layer1, self.w2) + self.b2)

        print(output)

        result = (output > 0.5).astype(np.int)
        print(result)

        return result


if __name__ == '__main__':
    model = Model()

    data = [i for i in range(13 * 16)]
    model.predict(data)

    np.save('../model/w1.npy', model.w1)
    np.save('../model/b1.npy', model.b1)
    np.save('../model/w2.npy', model.w2)
    np.save('../model/b2.npy', model.b2)
