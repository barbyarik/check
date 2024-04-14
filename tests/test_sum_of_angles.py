from pytest import approx
from math import sqrt
from r2point import R2Point
from convex import Figure, Void, Point, Segment, Polygon


class TestVoid:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Void()

    # Сумма углов пересечения нугольника и прямой всегда нулевая
    def test_area(self):
        assert self.f.angle_sum() == 0.0


class TestPoint:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Point(R2Point(0.0, 0.0))

    # Сумма углов пересечения точки и прямой всегда нулевая
    def test_area(self):
        assert self.f.angle_sum() == 0.0


class TestSegment1:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        Figure.POINT1 = R2Point(0.0, 0.0)
        Figure.POINT2 = R2Point(0.0, 10.0)
        self.f = Segment(R2Point(-1.0, 0.0), R2Point(1.0, 0.0))

    # Отрезок перпендикулярен прямой
    def test_angle90(self):
        assert self.f.angle_sum() == 90.0

    # Отрезок сонаправлен с прямой
    def test_angle0(self):
        Figure.POINT1 = R2Point(-5.0, 0.0)
        Figure.POINT2 = R2Point(5.0, 0.0)
        assert self.f.angle_sum() == 0.0

    # Отрезок не пересекает
    def test_angle_no_intersection(self):
        Figure.POINT1 = R2Point(-5.0, 2.0)
        Figure.POINT2 = R2Point(5.0, 2.0)
        assert self.f.angle_sum() == 0.0

    # Отрезок под произвольным углом к прямой
    def test_angle45(self):
        Figure.POINT1 = R2Point(0.0, 0.0)
        Figure.POINT2 = R2Point(2.0, 2.0)
        assert self.f.angle_sum() == 45.0


class TestPolygon:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        Figure.POINT1 = R2Point(0.0, 0.0)
        Figure.POINT2 = R2Point(0.0, 10.0)
        self.a = R2Point(-1.0, 0.0)
        self.b = R2Point(0.0, 1.0)
        self.c = R2Point(2.0, 0.0)
        self.f = Polygon(self.a, self.b, self.c)

    # многоугольник и прямая вида x = const
    def test_x_const(self):
        assert self.f.angle_sum() == 198.435

    # многоугольник и прямая вида y = const
    def test_y_const(self):
        Figure.POINT1 = R2Point(-5.0, 1.0)
        Figure.POINT2 = R2Point(5.0, 1.0)
        self.a = R2Point(-1.0, 0.0)
        self.b = R2Point(0.0, 1.0)
        self.c = R2Point(2.0, 0.0)
        self.f = Polygon(self.a, self.b, self.c)
        assert self.f.angle_sum() == 71.565

    # многоугольник и произвольная прямая
    def test_proisv(self):
        Figure.POINT1 = R2Point(-2.0, -1.0)
        Figure.POINT2 = R2Point(5.0, 4.0)
        self.a = R2Point(-1.0, 0.0)
        self.b = R2Point(0.0, 1.0)
        self.c = R2Point(2.0, 0.0)
        self.f = Polygon(self.a, self.b, self.c)
        assert self.f.angle_sum() == 97.641

    # многоугольник с добавленной точкой и прямая вида x = const
    def test_with_add_x_const(self):
        self.a = R2Point(-1.0, 0.0)
        self.b = R2Point(0.0, 1.0)
        self.c = R2Point(2.0, 0.0)
        self.f = Polygon(self.a, self.b, self.c)
        self.f.add(R2Point(0.0, -3.0))
        assert self.f.angle_sum() == 160.56

    # многоугольник с добавленной точкой и прямая вида y = const
    def test_with_add_y_const(self):
        Figure.POINT1 = R2Point(-5.0, 0.0)
        Figure.POINT2 = R2Point(5.0, 0.0)
        self.a = R2Point(-1.0, 0.0)
        self.b = R2Point(0.0, 1.0)
        self.c = R2Point(2.0, 0.0)
        self.f = Polygon(self.a, self.b, self.c)
        self.f.add(R2Point(0.0, -3.0))
        assert self.f.angle_sum() == 199.44

    def test_with_multi_add_proisv(self):
        Figure.POINT1 = R2Point(-1.0, 1.0)
        Figure.POINT2 = R2Point(1.0, -1.0)
        self.a = R2Point(-1.0, -1.0)
        self.b = R2Point(0.0, 3.0)
        self.c = R2Point(3.0, 3.0)
        self.f = Polygon(self.a, self.b, self.c)
        self.f.add(R2Point(3.0, 0.0))
        self.f.add(R2Point(-3.0, -3.0))
        assert self.f.angle_sum() == 143.13

    # многоугольник с добавленной точкой и произвольная прямая
    def test_with_add_proisv(self):
        Figure.POINT1 = R2Point(-2.0, -3.0)
        Figure.POINT2 = R2Point(1.0, 2.0)
        self.a = R2Point(-1.0, 0.0)
        self.b = R2Point(0.0, 1.0)
        self.c = R2Point(2.0, 0.0)
        self.f = Polygon(self.a, self.b, self.c)
        self.f.add(R2Point(0.0, -3.0))
        assert self.f.angle_sum() == 135.0
