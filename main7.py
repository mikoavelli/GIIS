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
        self._voronoi_points = []

        self._debug_mode = False
        self._debug_latency = 20

    def _create_menu(self):
        menubar = tk.Menu(self)
        menubar.add_command(label="Voronoi", command=self._voronoi)
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
        self._voronoi_points = []
        self._draw_grid()

    def _toggle_debug_mode(self):
        self._debug_mode = not self._debug_mode

    def _on_canvas_click(self, event):
        self._x = event.x // self._grid_size
        self._y = event.y // self._grid_size
        self._voronoi_points.append([self._x, self._y])
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
        if len(self._voronoi_points) < 2:
            messagebox.showerror("Error", "Not enough points to build voronoi.")
            return

        width = self._canvas.winfo_width() // self._grid_size
        height = self._canvas.winfo_height() // self._grid_size

        pixels = []
        for x in range(width):
            for y in range(height):
                closest_point_index = -1
                min_distance = float('inf')

                for i, (px, py) in enumerate(self._voronoi_points):
                    distance = math.sqrt((x - px)**2 + (y - py)**2)
                    if distance < min_distance:
                        min_distance = distance
                        closest_point_index = i

                if closest_point_index != -1:
                    random.seed(closest_point_index)
                    color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    pixels.append((x, y, color))

        self._draw_points(pixels)

def main():
    app = VoronoigApp()
    app.mainloop()


if __name__ == '__main__':
    main()
