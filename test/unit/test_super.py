class A:
    def method(self, arg):
        print(f'A: {arg}')


class B(A):
    def method(self, arg):
        super().method(arg)


def test():
    B().method('okok')
