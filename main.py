import tkinter as tk

from line_algorithms import (
    DDA,
    Bresenham,
    Wu
)
from curve_algorithms import (
    Circle,
    Ellipse,
    Hyperbola,
    Parabola
)


class DrawingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Drawing App")
        self.geometry("800x600")
        self._create_menu()
        self._create_canvas()

        self._grid_size = 20
        self._draw_grid()

        self._start_x = None
        self._start_y = None

        self.current_line_algorithm = None
        self.current_curve_algorithm = None
        self.debug_mode = False

    def _create_menu(self):
        menubar = tk.Menu(self)

        line_menu = tk.Menu(menubar, tearoff=0)
        line_menu.add_command(label="DDA", command=lambda: self._set_line_algorithm("DDA"))
        line_menu.add_command(label="Bresenham", command=lambda: self._set_line_algorithm("Bresenham"))
        line_menu.add_command(label="Wu", command=lambda: self._set_line_algorithm("Wu"))
        menubar.add_cascade(label="Line", menu=line_menu)

        curve_menu = tk.Menu(menubar, tearoff=0)
        curve_menu.add_command(label="Circle", command=lambda: self._set_curve_algorithm("Circle"))
        curve_menu.add_command(label="Hyperbola", command=lambda: self._set_curve_algorithm("Hyperbola"))
        curve_menu.add_command(label="Ellipse", command=lambda: self._set_curve_algorithm("Ellipse"))
        curve_menu.add_command(label="Parabola", command=lambda: self._set_curve_algorithm("Parabola"))
        menubar.add_cascade(label="Curve", menu=curve_menu)

        menubar.add_command(label="Clear", command=lambda: self._clear_canvas)

        menubar.add_command(label="Debug", command=self._toggle_debug_mode)

        self.config(menu=menubar)

    def _create_canvas(self):
        self._canvas = tk.Canvas(self, bg="white")
        self._canvas.pack(fill=tk.BOTH, expand=True)
        self._canvas.bind("<Button-1>", self._on_canvas_click)
        self._canvas.bind("<Configure>", lambda event: self._draw_grid())

    def _clear_canvas(self):
        self._canvas.delete("all")

    def _toggle_debug_mode(self):
        self.debug_mode = not self.debug_mode

    def _on_canvas_click(self, event):
        self._start_x = event.x // self._grid_size
        self._start_y = event.y // self._grid_size

        # print(self._start_x, self._start_y)

    def _draw_grid(self):
        self._canvas.delete("grid")
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        for x in range(0, width, self._grid_size):
            self._canvas.create_line(x, 0, x, height, fill="lightgray", tags="grid")

        for y in range(0, height, self._grid_size):
            self._canvas.create_line(0, y, width, y, fill="lightgray", tags="grid")

    def _set_line_algorithm(self, algorithm):
        self._uncheck_all_algorithms()

        match algorithm:
            case "DDA":
                self.current_line_algorithm = algorithm
                self.title("DDA")
            case "Bresenham":
                self.current_line_algorithm = algorithm
                self.title("Bresenham")
            case "Wu":
                self.current_line_algorithm = algorithm
                self.title("Wu")

    def _set_curve_algorithm(self, algorithm):
        self._uncheck_all_algorithms()

        match algorithm:
            case "Circle":
                self.current_curve_algorithm = algorithm
                self.title("Circle")
            case "Ellipse":
                self.current_curve_algorithm = algorithm
                self.title("Ellipse")
            case "Hyperbola":
                self.current_curve_algorithm = algorithm
                self.title("Hyperbola")
            case "Parabola":
                self.current_curve_algorithm = algorithm
                self.title("Parabola")

    def _uncheck_all_algorithms(self):
        self._current_line_algorithm = None
        self._current_curve_algorithm = None


def main():
    app = DrawingApp()
    app.mainloop()


if __name__ == '__main__':
    main()
