def Z(p):
    class Z:
        def __init__(self, x):
            self.x = x % p

        def __str__(self):
            return str(self.x)

        def __eq__(self, b):
            return self.x == b.x

        def __ne__(self, b):
            return self.x != b.x

        def __add__(self, b):
            return Z(self.x + b.x)

        def __sub__(self, b):
            return Z(self.x - b.x)

        def __mul__(self, b):
            return Z(self.x * b.x)

        def __truediv__(self, b):
            return self * Z(pow(b.x, p - 2, p))

        def __repr__(self):
            return str(self.x)

    return Z
