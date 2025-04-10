import tkinter as tk
from tkinter import messagebox

from scripts.line_algorithms import DDA, Bresenham, Wu
from scripts.polygon_algorithms import PolygonAlgorithm, Graham, Jarvis
from scripts.fill_algorithms import ET, AEL, Flood, LBL
from scripts.point_check import is_point_inside


class DrawingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Drawing App")
        self.geometry("800x600")
        self._create_menu()
        self._create_canvas()

        self._current_line_algorithm = None
        self._current_polygon_algorithm = None
        self._current_fill_algorithm = None
        self._fill_algorithm = {}

        self._points = []
        self.intersect_line = None
        self.intersect_point = None

        self._debug_mode = False
        self._debug_latency = 5

        self._canvas.bind("<Button-1>", self._add_point)

    def _create_menu(self):
        menubar = tk.Menu(self)

        line_menu = tk.Menu(menubar, tearoff=0)
        line_menu.add_command(label="DDA", command=lambda: self._set_line_algorithm("DDA"))
        line_menu.add_command(label="Bresenham", command=lambda: self._set_line_algorithm("Bresenham"))
        line_menu.add_command(label="Wu", command=lambda: self._set_line_algorithm("Wu"))
        menubar.add_cascade(label="Line", menu=line_menu)

        polygon_menu = tk.Menu(menubar, tearoff=0)
        polygon_menu.add_command(label="Graham", command=lambda: self._set_polygon_algorithm("Graham"))
        polygon_menu.add_command(label="Jarvis", command=lambda: self._set_polygon_algorithm("Jarvis"))
        polygon_menu.add_command(label="Is point in polygon", command=self._check_point_inside)
        polygon_menu.add_command(label="Check convexity", command=self._check_convexity)
        menubar.add_cascade(label="Polygon", menu=polygon_menu)

        fill_menu = tk.Menu(menubar, tearoff=0)
        fill_menu.add_command(label="ET", command=lambda: self._set_fill_algorithm('ET'))
        fill_menu.add_command(label="AEL", command=lambda: self._set_fill_algorithm('AEL'))
        fill_menu.add_command(label="Flood", command=lambda: self._set_fill_algorithm('Flood'))
        fill_menu.add_command(label="LBL", command=lambda: self._set_fill_algorithm('LBL'))
        menubar.add_cascade(label="Filling", menu=fill_menu)

        menubar.add_command(label="Find Intersection", command=self._find_intersection)
        menubar.add_command(label="Clear", command=self._clear_canvas)
        menubar.add_checkbutton(label="Debug", command=self._toggle_debug_mode)

        self.config(menu=menubar)

    def _create_canvas(self):
        self._canvas = tk.Canvas(self, bg="white")
        self._canvas.pack(fill=tk.BOTH, expand=True)

    def _clear_canvas(self):
        self._canvas.delete("all")
        self._points.clear()
        self.intersect_point = None
        self.intersect_line = None
        self._current_fill_algorithm = None
        self._fill_algorithm = {}

    def _toggle_debug_mode(self):
        self._debug_mode = not self._debug_mode

    def _add_point(self, event):
        x, y = event.x, event.y
        self._points.append((x, y))
        self._canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")
        if len(self._points) > 1:
            self._draw_points(*self._points[-2], *self._points[-1])

    def _draw_points(self, x0, y0, x1, y1, color="black"):
        if self._current_line_algorithm is None:
            messagebox.showerror("Error", "No line algorithm selected")
            return
        if x0 == x1 and y0 == y1:
            points = [(x0, y0, color)]
        else:
            algorithm = self._current_line_algorithm(x0, y0, x1, y1, color=color)
            points = algorithm.get_points()
        if self._debug_mode:
            self._draw_points_with_latency(points, 0)
            return

        for point in points:
            x, y, draw_color = point
            self._canvas.create_rectangle(x, y, x, y, outline=draw_color, fill=draw_color)

    def _draw_points_with_latency(self, points, index):
        if index >= len(points):
            return

        x, y, draw_color = points[index]
        self._canvas.create_rectangle(x, y, x, y, outline=draw_color, fill=draw_color)
        self.after(self._debug_latency, lambda: self._draw_points_with_latency(points, index + 1))

    """Other methods for lines and polygons"""

    def _set_line_algorithm(self, algorithm):
        match algorithm:
            case "DDA":
                self._current_line_algorithm = DDA
            case "Bresenham":
                self._current_line_algorithm = Bresenham
            case "Wu":
                self._current_line_algorithm = Wu

        self.title(algorithm)
        print(f"Selected line algorithm: {algorithm}")

    def _set_polygon_algorithm(self, algorithm):
        if len(self._points) < 3:
            messagebox.showerror("Error", "Not enough points to check polygon convex")
            return

        match algorithm:
            case "Graham":
                self._current_polygon_algorithm = Graham
            case "Jarvis":
                self._current_polygon_algorithm = Jarvis

        self.title(algorithm)
        print(f"Selected polygon algorithm: {algorithm}")
        self._draw_polygon()

    def _set_fill_algorithm(self, algorithm):
        if len(self._points) < 3:
            messagebox.showerror("Error", "First create a polygon")
            return

        match algorithm:
            case "ET":
                self._current_fill_algorithm = ET
            case "AEL":
                self._current_fill_algorithm = AEL
            case "Flood":
                self._current_fill_algorithm = Flood
            case "LBL":
                self._current_fill_algorithm = LBL

        self.title(algorithm)
        print(f"Selected polygon algorithm: {algorithm}")

        def on_click(event):
            x, y = event.x, event.y
            if not is_point_inside(self._points, x, y):
                messagebox.showerror("Error", "Point must be inside polygon")
            else:
                self._fill(x, y)

            self._canvas.unbind("<Button-1>")
            self._canvas.bind("<Button-1>", self._add_point)

        self._canvas.bind("<Button-1>", on_click)

    def _draw_polygon(self):
        algorithm = self._current_polygon_algorithm(self._points)
        points = algorithm.get_points()

        # self._canvas.delete("polygon")
        for i in range(len(points)):
            self._draw_points(*points[i], *points[(i + 1) % len(points)], color="red")

    def _fill(self, x, y):
        algorithm = self._current_fill_algorithm(self._points, x, y)
        points = algorithm.get_points()
        for i in range(len(points)):
            self._draw_points(*points[i], color="blue")

    def _check_convexity(self):
        if len(self._points) < 3:
            messagebox.showerror("Error", "Not enough points to check convexity")
            return

        normals = PolygonAlgorithm(self._points).check_convexity()
        if normals is None:
            messagebox.showinfo("Result", "Polygon is not convex")
        else:
            for normal in normals:
                self._draw_points(*normal, color="green")
            messagebox.showinfo("Result", "Polygon is convex")

    def _find_intersection(self):
        if len(self._points) < 3:
            messagebox.showerror("Error", "Not enough points to build polygon.")
            return

        if self.intersect_line:
            self._canvas.delete(self.intersect_line)
            self.intersect_line = None

        def on_first_click(event):
            self.intersect_point = (event.x, event.y)
            self._canvas.unbind("<Button-1>")
            self._canvas.bind("<Button-1>", on_second_click)

        def on_second_click(event):
            x1, y1 = self.intersect_point
            x2, y2 = event.x, event.y
            self._draw_points(x1, y1, x2, y2)
            self._canvas.unbind("<Button-1>")
            self._canvas.bind("<Button-1>", self._add_point)

            def calculate_intersection(p1, p2, poly):
                intersection_points = []
                x1, y1 = p1
                x2, y2 = p2
                for i in range(len(poly)):
                    x3, y3 = poly[i]
                    x4, y4 = poly[(i + 1) % len(poly)]

                    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                    if d == 0:
                        continue

                    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
                    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / d
                    if 0 <= t <= 1 and 0 <= u <= 1:
                        x = x1 + t * (x2 - x1)
                        y = y1 + t * (y2 - y1)
                        intersection_points.append((x, y))
                return intersection_points

            intersections = calculate_intersection((x1, y1), (x2, y2), self._points)
            if intersections:
                for intersection in intersections:
                    x, y = intersection
                    self._canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="red", tags="intersect")
                messagebox.showinfo("Result",
                                    f"Intersection points: {[f'({x:.2f}, {y:.2f})' for x, y in intersections]}")
            else:
                messagebox.showinfo("Result", "No intersections")
            self.intersect_line = self._canvas.create_line(x1, y1, x2, y2, fill="blue")

        self.title("Find Intersections")
        self._canvas.bind("<Button-1>", on_first_click)

    def _check_point_inside(self):
        if not self._points:
            messagebox.showerror("Error", "Polygon must be created.")
            return

        def on_click(event):
            x, y = event.x, event.y
            if is_point_inside(self._points, x, y):
                messagebox.showinfo("Result", f"Point ({x}, {y}) is in polygon.")
            else:
                messagebox.showinfo("Result", f"Point ({x}, {y}) is not in polygon.")
            self._canvas.unbind("<Button-1>")
            self._canvas.bind("<Button-1>", self._add_point)

        self._canvas.bind("<Button-1>", on_click)


def main():
    app = DrawingApp()
    app.mainloop()


if __name__ == '__main__':
    main()
