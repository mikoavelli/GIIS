import math
import random
import tkinter as tk
from tkinter import messagebox


class VoronoigApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Drawing App")
        self.geometry("800x600")
        self._create_menu()
        self._create_canvas()

        self._grid_size = 15
        self._draw_grid()

        self._x = None
        self._y = None
        self._points = []

        self._debug_mode = False
        self._debug_latency = 20

    def _create_menu(self):
        menubar = tk.Menu(self)
        menubar.add_command(label="Voronoi", command=self._voronoi)
        menubar.add_command(label="Delaunay", command=self._delaunay)
        menubar.add_command(label="Clear", command=self._clear_canvas)
        menubar.add_checkbutton(label="Debug", command=self._toggle_debug_mode)
        self.config(menu=menubar)

    def _create_canvas(self):
        self._canvas = tk.Canvas(self, bg="white")
        self._canvas.pack(fill=tk.BOTH, expand=True)
        self._canvas.bind("<Button-1>", self._on_canvas_click)
        self._canvas.bind("<Configure>", lambda event: self._draw_grid())

    def _draw_grid(self):
        self._canvas.delete("grid")
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        for x in range(0, width, self._grid_size):
            self._canvas.create_line(x, 0, x, height, fill="lightgray", tags="grid")

        for y in range(0, height, self._grid_size):
            self._canvas.create_line(0, y, width, y, fill="lightgray", tags="grid")

    def _clear_canvas(self):
        self._canvas.delete("all")
        self._points = []
        self._draw_grid()

    def _toggle_debug_mode(self):
        self._debug_mode = not self._debug_mode

    def _on_canvas_click(self, event):
        self._x = event.x // self._grid_size
        self._y = event.y // self._grid_size
        self._points.append([self._x, self._y])
        self._canvas.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3, fill="red")

    def _draw_points_with_latency(self, points, index):
        if index >= len(points):
            return
        x, y, color = points[index]
        self._canvas.create_rectangle(
            x * self._grid_size,
            y * self._grid_size,
            (x + 1) * self._grid_size,
            (y + 1) * self._grid_size,
            outline="black",
            fill=color
        )
        print(f"Point: {x:5} {y:5}")
        self.after(self._debug_latency, lambda: self._draw_points_with_latency(points, index + 1))

    def _draw_points(self, points):
        if not self._debug_mode:
            for point in points:
                x, y, color = point
                self._canvas.create_rectangle(
                    x * self._grid_size,
                    y * self._grid_size,
                    (x + 1) * self._grid_size,
                    (y + 1) * self._grid_size,
                    outline='black',
                    fill=color
                )
        else:
            self._draw_points_with_latency(points, 0)

    def _voronoi(self):
        if len(self._points) < 2:
            messagebox.showerror("Error", "Not enough points to build voronoi.")
            return

        width = self._canvas.winfo_width() // self._grid_size
        height = self._canvas.winfo_height() // self._grid_size

        pixels = []
        for x in range(width):
            for y in range(height):
                closest_point_index = -1
                min_distance = float('inf')

                for i, (px, py) in enumerate(self._points):
                    distance = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                    if distance < min_distance:
                        min_distance = distance
                        closest_point_index = i

                if closest_point_index != -1:
                    random.seed(closest_point_index)
                    color = "#{:02x}{:02x}{:02x}".format(
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255))
                    pixels.append((x, y, color))

        self._draw_points(pixels)

    def _delaunay(self):
        if len(self._points) < 3:
            messagebox.showerror("Error", "Not enough points to build Delaunay triangulation.")
            return

        points = [tuple(pt) for pt in self._points]

        def circumcircle(tri):
            (ax, ay), (bx, by), (cx, cy) = tri
            d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
            if d == 0:
                return None, None, None
            ux = ((ax * ax + ay * ay) * (by - cy) +
                  (bx * bx + by * by) * (cy - ay) +
                  (cx * cx + cy * cy) * (ay - by)) / d
            uy = ((ax * ax + ay * ay) * (cx - bx) +
                  (bx * bx + by * by) * (ax - cx) +
                  (cx * cx + cy * cy) * (bx - ax)) / d
            r = math.hypot(ax - ux, ay - uy)
            return ux, uy, r

        def triangle_edges(tri):
            p, q, r = tri
            edge1 = tuple(sorted((p, q)))
            edge2 = tuple(sorted((q, r)))
            edge3 = tuple(sorted((r, p)))
            return [edge1, edge2, edge3]

        min_x = min(p[0] for p in points)
        min_y = min(p[1] for p in points)
        max_x = max(p[0] for p in points)
        max_y = max(p[1] for p in points)
        dx = max_x - min_x
        dy = max_y - min_y
        delta_max = max(dx, dy)
        mid_x = (min_x + max_x) / 2
        mid_y = (min_y + max_y) / 2

        p1 = (mid_x - 2 * delta_max, mid_y - delta_max)
        p2 = (mid_x, mid_y + 2 * delta_max)
        p3 = (mid_x + 2 * delta_max, mid_y - delta_max)
        super_triangle = (p1, p2, p3)

        triangles = [super_triangle]

        for p in points:
            bad_triangles = []
            for tri in triangles:
                cc = circumcircle(tri)
                if cc[0] is None:
                    continue
                ux, uy, r = cc
                if math.hypot(p[0] - ux, p[1] - uy) <= r:
                    bad_triangles.append(tri)

            edge_count = {}
            for tri in bad_triangles:
                for edge in triangle_edges(tri):
                    edge_count[edge] = edge_count.get(edge, 0) + 1

            polygon = [edge for edge, count in edge_count.items() if count == 1]

            triangles = [tri for tri in triangles if tri not in bad_triangles]

            for edge in polygon:
                new_triangle = (edge[0], edge[1], p)
                triangles.append(new_triangle)

        triangles = [tri for tri in triangles if p1 not in tri and p2 not in tri and p3 not in tri]

        drawn_edges = set()
        for tri in triangles:
            for edge in triangle_edges(tri):
                if edge not in drawn_edges:
                    drawn_edges.add(edge)
                    (x1, y1), (x2, y2) = edge
                    canvas_x1 = x1 * self._grid_size + self._grid_size / 2
                    canvas_y1 = y1 * self._grid_size + self._grid_size / 2
                    canvas_x2 = x2 * self._grid_size + self._grid_size / 2
                    canvas_y2 = y2 * self._grid_size + self._grid_size / 2
                    self._canvas.create_line(canvas_x1, canvas_y1, canvas_x2, canvas_y2, fill="blue", width=2)


def main():
    app = VoronoigApp()
    app.mainloop()


if __name__ == '__main__':
    main()
