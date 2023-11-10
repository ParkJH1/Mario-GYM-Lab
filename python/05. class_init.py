class A:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def f(self):
        print(self.a)
        print(self.b)
        print(self.c)


if __name__ == '__main__':
    a = A(10, 'abcd', [5, 6, 7])
    a.f()
