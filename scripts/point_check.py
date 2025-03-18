def is_point_inside(points, x, y):
    if len(points) < 3:
        return False

    n = len(points)
    inside = False

    for i in range(n):
        p1 = points[i]
        p2 = points[(i + 1) % n]

        if point_on_segment((x, y), p1, p2):
            return True

        if (p1[1] > y) != (p2[1] > y):
            try:
                x_inters = ((y - p1[1]) * (p2[0] - p1[0])) / (p2[1] - p1[1]) + p1[0]
            except ZeroDivisionError:
                continue

            if x <= x_inters:
                inside = not inside

    return inside


def point_on_segment(pt, p1, p2):
    x, y = pt
    x1, y1 = p1
    x2, y2 = p2

    if (x < min(x1, x2) - 1e-8 or x > max(x1, x2) + 1e-8 or
            y < min(y1, y2) - 1e-8 or y > max(y1, y2) + 1e-8):
        return False

    cross_product = (x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)
    if abs(cross_product) > 1e-8:
        return False

    return True


def is_on_boundary(points, x, y):
    """Проверяет, находится ли точка на границе полигона"""
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]
        if point_on_segment((x, y), p1, p2):
            return True
    return False


def point_on_segment(pt, p1, p2):
    x, y = pt
    x1, y1 = p1
    x2, y2 = p2

    if (x < min(x1, x2) - 1e-8 or x > max(x1, x2) + 1e-8 or
            y < min(y1, y2) - 1e-8 or y > max(y1, y2) + 1e-8):
        return False

    cross_product = (x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)
    if abs(cross_product) > 1e-8:
        return False

    return True
