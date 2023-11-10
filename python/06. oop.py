class Parent:
    def __init__(self, a, child):
        print('Parent init')
        self.a = a
        self.child = child

    def f(self):
        print('Parent f')
        self.child.f1()


class Child(Parent):
    def __init__(self, a, b, c):
        print('Child init before')
        super().__init__(a, self)
        print('Child init after')
        self.b = b
        self.c = c

    def f1(self):
        print('============')
        print('Child f1')
        print(self.a)
        print(self.b)
        print(self.c)
        print('============')

    def f2(self):
        print('------------')
        print('Child f2')
        self.f()
        print('------------')


if __name__ == '__main__':
    c = Child(10, 'abcd', [5, 6, 7])
    c.f1()
    c.f2()
