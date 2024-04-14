from deq import Deq
from r2point import R2Point
from math import sqrt, acos, degrees, pi


def sgnn(num):
    return 1 if num > 0 else 0 if num == 0 else -1


class Figure:
    """ Абстрактная фигура """

    POINT1 = R2Point(1, 1)
    POINT2 = R2Point(-1, -1)

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    def angle_sum(self):  # NEW
        return 0.0

    @staticmethod  # NEW
    def intersection(line_point1, line_point2, p, q):
        x1, y1 = line_point1.x, line_point1.y
        x2, y2 = line_point2.x, line_point2.y
        C = -x1 * y2 + y1 * x2
        a = p.x * (y2 - y1) - p.y * (x2 - x1)
        b = q.x * (y2 - y1) - q.y * (x2 - x1)
        if C <= 0:
            return (sgnn(a + C) != sgnn(b + C)) or \
                sgnn(a + C) == 0 or sgnn(b + C) == 0
        else:
            return (sgnn(-a - C) != sgnn(-b - C)) or \
                sgnn(a + C) == 0 or sgnn(b + C) == 0

    @staticmethod  # NEW
    def ang(line_point1, line_point2, p, q):
        scal = (p.x - q.x) * (line_point1.x - line_point2.x) +\
            (p.y - q.y) * (line_point1.y - line_point2.y)
        ang_intermediate = abs(scal / (sqrt((p.x - q.x) ** 2 +
                                            (p.y - q.y) ** 2)
                               * sqrt((line_point1.x - line_point2.x) **
                                      2 + (line_point1.y -
                                           line_point2.y) ** 2)))
        answer = degrees(min(acos(ang_intermediate), pi -
                             acos(ang_intermediate)))
        return round(answer, 3)


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        return Point(p)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p):
        self.p = p

    def add(self, q):
        return self if self.p == q else Segment(self.p, q)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        self.p, self.q = p, q

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def angle_sum(self):  # NEW
        if self.intersection(Figure.POINT1, Figure.POINT2, self.p, self.q):
            return self.ang(Figure.POINT1, Figure.POINT2, self.p, self.q)
        else:
            return 0.0

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r)
        elif r.is_inside(self.p, self.q):
            return self
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q)
        else:
            return Segment(self.p, r)


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c):
        self.points = Deq()
        self.points.push_first(b)
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))
        # NEW
        answer = 0.0
        for i in range(self.points.size()):
            if self.intersection(Figure.POINT1, Figure.POINT2,
                                 self.points.first(), self.points.last()):
                answer += self.ang(Figure.POINT1, Figure.POINT2,
                                   self.points.first(), self.points.last())
            self.points.push_last(self.points.pop_first())
        self._angle_sum = round(answer, 3)

    def perimeter(self):
        return self._perimeter

    def angle_sum(self):  # NEW
        return self._angle_sum

    def area(self):
        return self._area

    # добавление новой точки
    def add(self, t):
        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())
        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):
            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))
            if self.intersection(Figure.POINT1, Figure.POINT2,
                                 self.points.last(), self.points.first()):
                self._angle_sum -= self.ang(Figure.POINT1, Figure.POINT2,
                                            self.points.first(),
                                            self.points.last())  # NEW
            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                if self.intersection(Figure.POINT1, Figure.POINT2,
                                     self.points.first(), p):
                    self._angle_sum -= self.ang(Figure.POINT1,
                                                Figure.POINT2,
                                                self.points.first(),
                                                p)  # NEW
                p = self.points.pop_first()
            self.points.push_first(p)
            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                if self.intersection(Figure.POINT1,
                                     Figure.POINT2,
                                     self.points.last(),
                                     p):
                    self._angle_sum -= self.ang(Figure.POINT1,
                                                Figure.POINT2,
                                                self.points.last(),
                                                p)  # NEW
                p = self.points.pop_last()
            self.points.push_last(p)
            # добавление двух новых рёбер
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())
            if self.intersection(Figure.POINT1, Figure.POINT2,
                                 self.points.first(), t):
                self._angle_sum += self.ang(Figure.POINT1, Figure.POINT2,
                                            self.points.first(), t)  # NEW
            if self.intersection(Figure.POINT1, Figure.POINT2,
                                 self.points.last(), t):
                self._angle_sum += self.ang(Figure.POINT1, Figure.POINT2,
                                            self.points.last(), t)  # NEW
            self.points.push_first(t)
            self._angle_sum = round(self._angle_sum, 3)
        return self
