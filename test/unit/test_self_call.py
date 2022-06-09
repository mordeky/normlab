class A:
    def __init__(self):
        self.x = 3

    def do(self):
        print(self.x)

    def __call__(self, *args, **kwargs):
        x = A()
        x.do()


def test_self_call():
    print()
    A()()
