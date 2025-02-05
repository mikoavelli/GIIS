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
        # Определяем концевые точки
        p0 = (self.x0, self.y0)
        p1 = (self.x1, self.y1)
        # Вычисляем разность между точками
        dx = self.x1 - self.x0
        dy = self.y1 - self.y0
        # Для получения кривой выбираем касательные, направленные перпендикулярно от прямой
        t0 = (-dy / 3, dx / 3)
        t1 = (dy / 3, -dx / 3)

        result = []
        # Дискретизация параметра t от 0 до 1 с шагом 0.01
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
        # Определяем управляющие точки с небольшим смещением для создания кривизны
        p1 = (self.x0 + dx / 3 - dy / 10, self.y0 + dy / 3 + dx / 10)
        p2 = (self.x0 + 2 * dx / 3 - dy / 10, self.y0 + 2 * dy / 3 + dx / 10)

        result = []
        # Дискретизация параметра t с шагом 0.0001
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
        dx = self.x1 - self.x0
        dy = self.y1 - self.y0
        # Формируем 4 контрольные точки, добавляя смещение для кривизны
        p0 = (self.x0, self.y0)
        p1 = (self.x0 + dx / 3 + dy / 10, self.y0 + dy / 3 - dx / 10)
        p2 = (self.x0 + 2 * dx / 3 + dy / 10, self.y0 + 2 * dy / 3 - dx / 10)
        p3 = (self.x1, self.y1)

        result = []
        # Дискретизация параметра t от 0 до 1 с шагом 0.01
        for t in [x / 100 for x in range(101)]:
            x = ((-t ** 3 + 3 * t ** 2 - 3 * t + 1) / 6 * p0[0] +
                 (3 * t ** 3 - 6 * t ** 2 + 4) / 6 * p1[0] +
                 (-3 * t ** 3 + 3 * t ** 2 + 3 * t + 1) / 6 * p2[0] +
                 (t ** 3) / 6 * p3[0])
            y = ((-t ** 3 + 3 * t ** 2 - 3 * t + 1) / 6 * p0[1] +
                 (3 * t ** 3 - 6 * t ** 2 + 4) / 6 * p1[1] +
                 (-3 * t ** 3 + 3 * t ** 2 + 3 * t + 1) / 6 * p2[1] +
                 (t ** 3) / 6 * p3[1])
            result.append((int(x), int(y), self.color))
        return result
