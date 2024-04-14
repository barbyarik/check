#!/usr/bin/env -S python3 -B
from tk_drawer import TkDrawer
from r2point import R2Point
from convex import Figure, Void, Point, Segment, Polygon


def void_draw(self, tk):
    pass


def point_draw(self, tk):
    tk.draw_point(self.p)


def segment_draw(self, tk):
    tk.draw_line(self.p, self.q)


def polygon_draw(self, tk):
    for n in range(self.points.size()):
        tk.draw_line(self.points.last(), self.points.first())
        self.points.push_last(self.points.pop_first())


def draw_main_line(p, q):
    x1, y1, x2, y2 = p.x, p.y, q.x, q.y
    if x2 == x1:
        tk.draw_line(R2Point(x1, -12), R2Point(x1, 12))
    elif y2 == y1:
        tk.draw_line(R2Point(-12, y1), R2Point(12, y2))
    else:
        tk.draw_line(R2Point(-12, (-12 - x1)*(y2 - y1)/(x2 - x1) + y1),
                     R2Point(12, (12 - x1)*(y2 - y1)/(x2 - x1) + y1))


setattr(Void, 'draw', void_draw)
setattr(Point, 'draw', point_draw)
setattr(Segment, 'draw', segment_draw)
setattr(Polygon, 'draw', polygon_draw)


tk = TkDrawer()
f = Void()
tk.clean()

Figure.POINT1 = R2Point(float(input('x1: ')), float(input('y1: ')))
Figure.POINT2 = R2Point(float(input('x2: ')), float(input('y2: ')))

draw_main_line(f.POINT1, f.POINT2)

try:
    while True:
        f = f.add(R2Point())
        tk.clean()
        draw_main_line(f.POINT1, f.POINT2)
        f.draw(tk)
        print(f"S = {f.area()}, P = {f.perimeter()}", end='')
        print(f", sum of angles = {f.angle_sum()}\n")
except (EOFError, KeyboardInterrupt):
    print("\nStop")
    tk.close()
