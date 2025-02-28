import numpy as np


class Polygon:
    def __init__(self, points):
        self.points = points

    def _get_internal_normals(self):
        normals = []
        n = len(self.points)
        for i in range(n):
            p1, p2 = self.points[i], self.points[(i + 1) % n]
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            normals.append((-dy, dx))
        return normals

    def _draw_normals(self, normals):
        if not normals:
            return

        result = []

        for i, p in enumerate(self.points):
            normal = normals[i]
            center_x = (self.points[i][0] + self.points[(i + 1) % len(self.points)][0]) / 2
            center_y = (self.points[i][1] + self.points[(i + 1) % len(self.points)][1]) / 2
            result.append((center_x, center_y, center_x + normal[0] * 20, center_y + normal[1] * 20))

        return tuple(result)

    def check_convexity(self):
        def cross_product(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

        signs = []
        n = len(self.points)
        for i in range(n):
            o, a, b = self.points[i], self.points[(i + 1) % n], self.points[(i + 2) % n]
            signs.append(np.sign(cross_product(o, a, b)))

        if all(s >= 0 for s in signs) or all(s <= 0 for s in signs):
            normals = self._get_internal_normals()
            return self._draw_normals(normals)
        else:
            return None


class Graham(Polygon):
    def get_points(self):
        points = sorted(self.points, key=lambda p: (p[0], p[1]))

        def cross(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

        lower = []
        for p in points:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)
        upper = []
        for p in reversed(points):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)
        hull = lower[:-1] + upper[:-1]
        return hull


class Jarvis(Polygon):
    def get_points(self):
        def orientation(p, q, r):
            return (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

        hull = []
        leftmost = min(self.points, key=lambda p: p[0])
        p = leftmost
        while True:
            hull.append(p)
            q = self.points[0]
            for r in self.points:
                if q == p or orientation(p, q, r) < 0:
                    q = r
            p = q
            if p == leftmost:
                break
        return hull
