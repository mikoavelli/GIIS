from scripts.point_check import is_point_inside, is_on_boundary


class FillAlgorithm:
    def __init__(self, points, x, y):
        self._points = points
        self._start_x = x
        self._start_y = y
        self._fill_algorithm_state = {}


class ET(FillAlgorithm):
    def get_points(self):
        points = []

        et = {}
        for i in range(len(self._points)):
            p1 = self._points[i]
            p2 = self._points[(i + 1) % len(self._points)]

            if p1[1] == p2[1]:
                continue

            if p1[1] > p2[1]:
                p1, p2 = p2, p1

            y_min = int(p1[1])
            y_max = int(p2[1])
            x = p1[0]
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]

            if dy == 0:
                continue

            slope = dx / dy

            if y_min not in et:
                et[y_min] = []
            et[y_min].append({
                'y_max': y_max,
                'x': x,
                'dx': dx,
                'dy': dy,
                'slope': slope
            })

        if not et:
            return

        ael = []
        current_y = min(et.keys())

        while True:
            if current_y in et:
                for edge in et[current_y]:
                    ael.append(edge)
                del et[current_y]

            ael.sort(key=lambda e: e['x'])
            i = 0
            while i < len(ael):
                e1 = ael[i]
                if i + 1 >= len(ael):
                    break

                e2 = ael[i + 1]
                x_start = int(e1['x'])
                x_end = int(e2['x'])

                if x_start > x_end:
                    x_start, x_end = x_end, x_start

                points.append((x_start, current_y, x_end, current_y))
                i += 2

            current_y += 1
            ael = [e for e in ael if e['y_max'] > current_y]

            for edge in ael:
                edge['x'] += edge['slope']

            if not ael and not et:
                break

        return points


class AEL(FillAlgorithm):
    def get_points(self):
        points = []

        et = {}
        for i in range(len(self._points)):
            p1 = self._points[i]
            p2 = self._points[(i + 1) % len(self._points)]

            if p1[1] == p2[1]:
                continue

            if p1[1] > p2[1]:
                p1, p2 = p2, p1

            y_min = int(p1[1])
            y_max = int(p2[1])
            x = p1[0]
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            slope = dx / dy

            if y_min not in et:
                et[y_min] = []
            et[y_min].append({'y_max': y_max, 'x': x, 'slope': slope})

        ael = []
        current_y = min(et.keys()) if et else 0

        while True:
            if current_y in et:
                ael.extend(et[current_y])
                del et[current_y]

            ael.sort(key=lambda e: e['x'])

            i = 0
            while i < len(ael):
                if i + 1 >= len(ael):
                    break
                e1 = ael[i]
                e2 = ael[i + 1]
                x_start = int(e1['x'])
                x_end = int(e2['x'])
                if x_start < x_end:
                    points.append((x_start, current_y, x_end, current_y))
                i += 2

            current_y += 1
            new_ael = []
            for edge in ael:
                if edge['y_max'] > current_y:
                    edge['x'] += edge['slope']
                    new_ael.append(edge)
            ael = new_ael

            if not ael and not et:
                break

        return points


class Flood(FillAlgorithm):
    def get_points(self):
        points = []

        stack = [(self._start_x, self._start_y)]
        filled = set()

        while stack:
            x, y = stack.pop()
            if (x, y) in filled:
                continue
            if not is_point_inside(self._points, x, y) or is_on_boundary(self._points, x, y):
                continue

            points.append((x, y, x + 1, y + 1))
            filled.add((x, y))

            stack.append((x + 1, y))
            stack.append((x - 1, y))
            stack.append((x, y + 1))
            stack.append((x, y - 1))

        return points


class LBL(FillAlgorithm):
    def get_points(self):
        points = []

        min_y = min(p[1] for p in self._points)
        max_y = max(p[1] for p in self._points)

        for current_y in range(int(min_y), int(max_y) + 1):
            intersections = []
            for i in range(len(self._points)):
                p1 = self._points[i]
                p2 = self._points[(i + 1) % len(self._points)]

                if (p1[1] <= current_y < p2[1]) or (p2[1] <= current_y < p1[1]):
                    x_intersect = (current_y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]
                    intersections.append(x_intersect)

            intersections.sort()

            for i in range(0, len(intersections) - 1, 2):
                x1 = int(intersections[i])
                x2 = int(intersections[i + 1])
                for x in range(x1, x2 + 1):
                    if is_point_inside(self._points, x, current_y):
                        points.append((x, current_y, x + 1, current_y + 1))

        return points
