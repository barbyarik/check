#!/usr/bin/env -S python3 -B
from r2point import R2Point
from convex import Figure, Void

f = Void()
Figure.POINT1 = R2Point(float(input('x1: ')), float(input('y1: ')))
Figure.POINT2 = R2Point(float(input('x2: ')), float(input('y2: ')))

try:
    while True:
        f = f.add(R2Point())
        print(f"S = {f.area()}, P = {f.perimeter()}", end='')
        print(f", sum of angles = {f.angle_sum()}\n")
except (EOFError, KeyboardInterrupt):
    print("\nStop")
