from tkinter import Tk, BOTH, Canvas
import time


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

    def __repr__(self) -> str:
        return f"cell {self._x1} {self._y1}"

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

    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win: Window, ) -> None:
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.cells = []

    def create_cells(self):
        for i in range(self.num_cols):
            cells = []
            for _ in range(self.num_rows):
                cell = Cell(self.x1, self.y1, self.cell_size_x, self.cell_size_y, self.win)
                cells.append(cell)
            self.cells.append(cells)

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.draw(i, j)

    def draw(self, i, j):
        x_cord = self.x1 + i * self.cell_size_x
        y_cord = self.y1 + j * self.cell_size_y

        cell = self.cells[i][j]
        cell.draw(x_cord, y_cord, self.x1, self.y1)
        self.animate()

    def animate(self):
        self.win.redraw()
        time.sleep(0.05)
        

def main():
    win = Window(800, 600)

    x1 = 5  # starting x position of the maze
    y1 = 5  # starting y position of the maze
    num_rows = 12  # number of rows in the maze
    num_cols = 11  # number of columns in the maze
    cell_size_x = 10  # width of each cell
    cell_size_y = 10  # height of each cell
    

    # Create and draw the maze
    maze = Maze(x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win)
    print(len(maze.cells))
    maze.create_cells()
    print(len(maze.cells))
    print(maze.cells)

    win.wait_for_close()


if __name__ == "__main__":
    main()
