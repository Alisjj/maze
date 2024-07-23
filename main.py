from tkinter import Tk, BOTH, Canvas


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2) -> None:
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )


class Window:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas()
        self.canvas.pack()
        self.running = False

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.canvas, fill_color)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False


class Cell:
    def __init__(
        self,
        _x1,
        _x2,
        _y1,
        _y2,
        _win: Window,
        has_left_wall=True,
        has_right_wall=True,
        has_top_wall=True,
        has_bottom_wall=True,
    ) -> None:
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._x1 = _x1
        self._x2 = _x2
        self._y1 = _y1
        self._y2 = _y2
        self._win = _win

    def draw(self, x1, y1, x2, y2):
        p1 = Point(x1, y1)
        p2 = Point(x2, y2)
        p3 = Point(x2, y1)
        p4 = Point(x1, y2)
        left_wall = Line(p1, p4)
        right_wall = Line(p3, p2)
        top_wall = Line(p1, p3)
        bottom_wall = Line(p4, p2)
        if self.has_left_wall:
            self._win.draw_line(left_wall, "white")

        if self.has_right_wall:
            self._win.draw_line(right_wall, "white")

        if self.has_top_wall:
            self._win.draw_line(top_wall, "white")

        if self.has_bottom_wall:
            self._win.draw_line(bottom_wall, "white")

    def draw_move(self, to_cell, undo=False):
        self_center_x = self._x1 + ((self._x2 - self._x1) / 2)
        self_center_y = self._y1 + ((self._y2 - self._y1) / 2)
        center_self = Point(self_center_x, self_center_y)

        other_center_x = to_cell._x1 + ((to_cell._x2 - to_cell._x1) / 2)
        other_center_y = to_cell._y1 + ((to_cell._y2 - to_cell._y1) / 2)
        center_other = Point(other_center_x, other_center_y)

        line = Line(center_self, center_other)
        color = "grey" if undo else "red"
        self._win.draw_line(line, color)


class Maze:

    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win, ) -> None:
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.cells = []

    def create_cells(self):
        cell = Cell(self.x1, self.y1, self.cell_size_x, self.cell_size_y, self.win)
        for _ in range(1, self.num_cols + 1):
            for j in range(1, self.num_rows + 1):
                self.cells.append(cell)

def main():
    win = Window(800, 600)

    x1_cell1, y1_cell1 = 50, 50
    x2_cell1, y2_cell1 = 100, 100

    # Coordinates for the second cell (to the right of the first cell)
    x1_cell2, y1_cell2 = 100, 50
    x2_cell2, y2_cell2 = 150, 100

    # Create instances of the Cell class
    cell1 = Cell(x1_cell1, x2_cell1, y1_cell1, y2_cell1, win)
    cell2 = Cell(x1_cell2, x2_cell2, y1_cell2, y2_cell2, win)

    # Draw the cells
    cell1.draw(x1_cell1, y1_cell1, x2_cell1, y2_cell1)
    cell2.draw(x1_cell2, y1_cell2, x2_cell2, y2_cell2)

    cell1.draw_move(cell2)

    win.wait_for_close()


if __name__ == "__main__":
    main()
