from collections import namedtuple

from cyclic_group import Z

Point = namedtuple('Point', ['x', 'y'])


class EdwardsCurves:
    """ x**2 + y**2 = 1 + d * x**2 * y**2 (mod p) """

    def __init__(self, d, p):
        self.z = Z(p)
        self.p = p
        self.d = self.process_d(d)
        self.one = self.z(1)
        self.zero = self.z(0)

    def process_d(self, d):
        """
        Prepares d for further process. d can be specified as int or as fraction (str)
        Example:
        d = 5
        or
        d = '5/9'
        """
        if type(d) == str:
            data = d.split('/')
            return self.z(int(data[0])) / self.z(int(data[1]))
        return self.z(d)

    def add_points(self, p1, p2):
        """ Adds two points on curve. Returns sum of these points which is also on curve """
        x1, y1 = p1
        x2, y2 = p2
        x3 = (x1 * y2 + y1 * x2) / (self.one + self.d * x1 * y1 * x2 * y2)
        y3 = (y1 * y2 - x1 * x2) / (self.one - self.d * x1 * y1 * x2 * y2)
        return self.create_point(x3.x, y3.x)

    def scalar_mul(self, scalar, point):
        """
        Multiplies point by scalar. In normal arithmetic:
        5 * <1, 2> = <5, 10>
        """
        if scalar == 0:
            return self.create_point(0, 1)
        if scalar == 1:
            return point
        Q = self.scalar_mul(scalar // 2, point)
        Q = self.add_points(Q, Q)
        if scalar % 2:
            Q = self.add_points(Q, point)
        return Q

    def neg(self, p):
        """ Negates point, example: (1, 0) == (p - 1, 0) """
        return self.create_point(-p.x.x, p.y.x)

    def create_point(self, x, y):
        """ Creates point with cyclic group properties """
        x = self.z(x)
        y = self.z(y)
        return Point(x, y)

    def is_on_curve(self, p):
        """ Checks if point p is on curve """
        x, y = p
        x, y = x.x, y.x
        return (x ** 2 + y ** 2) % self.p == (1 + self.d.x * x ** 2 * y ** 2) % self.p

    def order(self, g):
        """
        Return order of point g. In other words returns minimum scalar so that
        scalar * g == base_point. In case of Edwards Curve given by formula
        x**2 + y**2 = 1 + d * x**2 * y**2 (mod p)
        base point = Point(0, 1)
        """
        base_point = self.create_point(0, 1)
        assert self.is_on_curve(g)
        assert g != base_point
        for i in range(2, self.p):
            if self.scalar_mul(i, g) == base_point:
                return i
        return 1
