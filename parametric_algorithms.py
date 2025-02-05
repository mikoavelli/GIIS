import math


class ParametricAlgorithm:
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.color = "black"

    def get_points(self):
        pass


class HermiteAlgorithm(ParametricAlgorithm):
    def get_points(self):
        p0 = (self.x0, self.y0)
        p1 = (self.x1, self.y1)
        dx = self.x1 - self.x0
        dy = self.y1 - self.y0
        t0 = (-dy / 3, dx / 3)
        t1 = (dy / 3, -dx / 3)

        result = []
        for t in [x / 100 for x in range(101)]:
            h1 = 2 * t ** 3 - 3 * t ** 2 + 1
            h2 = -2 * t ** 3 + 3 * t ** 2
            h3 = t ** 3 - 2 * t ** 2 + t
            h4 = t ** 3 - t ** 2

            x = h1 * p0[0] + h2 * p1[0] + h3 * t0[0] + h4 * t1[0]
            y = h1 * p0[1] + h2 * p1[1] + h3 * t0[1] + h4 * t1[1]
            result.append((int(x), int(y), self.color))
        return result


class BezierAlgorithm(ParametricAlgorithm):
    def get_points(self):
        p0 = (self.x0, self.y0)
        p3 = (self.x1, self.y1)
        dx = self.x1 - self.x0
        dy = self.y1 - self.y0
        p1 = (self.x0 + dx / 3 - dy / 10, self.y0 + dy / 3 + dx / 10)
        p2 = (self.x0 + 2 * dx / 3 - dy / 10, self.y0 + 2 * dy / 3 + dx / 10)

        result = []
        for j in range(10001):
            t = j / 10000
            x = ((1 - t) ** 3) * p0[0] + 3 * ((1 - t) ** 2) * t * p1[0] + 3 * (1 - t) * (t ** 2) * p2[0] + (t ** 3) * \
                p3[0]
            y = ((1 - t) ** 3) * p0[1] + 3 * ((1 - t) ** 2) * t * p1[1] + 3 * (1 - t) * (t ** 2) * p2[1] + (t ** 3) * \
                p3[1]
            result.append((int(x), int(y), self.color))
        return result


class BSplineAlgorithm(ParametricAlgorithm):
    def get_points(self):
        pass
