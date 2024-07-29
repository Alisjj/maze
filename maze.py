import random
import time

from cell import Cell
from widgets import Window


class Maze:

    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ) -> None:
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.cells: list[Cell] = []
        self.seed = seed
        if seed:
            random.seed(self.seed)

        self.create_cells()
        self.break_entrance_and_exit()
        self.break_walls_r(0, 0)
        self.reset_cells_visited()

    def create_cells(self):
        for i in range(self.num_cols):
            cells = []
            for _ in range(self.num_rows):
                cell = Cell( self.win )
                cells.append(cell)
            self.cells.append(cells)

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.draw_cell(i, j)

    def draw_cell(self, i, j):
        if self.win is None:
            return
        x1 = self.x1 + i * self.cell_size_x
        y1 = self.y1 + j * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self.cells[i][j].draw(x1, y1, x2, y2)
        self.animate()

    def animate(self):
        self.win.redraw()
        time.sleep(0.05)

    def break_entrance_and_exit(self):
        top_left_cell: Cell = self.cells[0][0]
        bottom_right_cell: Cell = self.cells[self.num_cols - 1][self.num_rows - 1]

        top_left_cell.has_left_wall = False
        self.draw_cell(0, 0)
        bottom_right_cell.has_right_wall = False
        self.draw_cell(self.num_cols - 1, self.num_rows - 1)
        

    def break_walls_r(self, i, j):
        current_cell: Cell = self.cells[i][j]
        current_cell.visited = True

        while True:
            p_directions = []

            # left
            if i > 0 and not self.cells[i - 1][j].visited:
                p_directions.append((i - 1, j))

            # right
            if i < self.num_cols - 1 and not self.cells[i + 1][j].visited:
                p_directions.append((i + 1, j))

            # top
            if j > 0 and not self.cells[i][j - 1].visited:
                p_directions.append((i, j - 1))

            # buttom
            if j < self.num_rows - 1 and not self.cells[i][j + 1].visited:
                p_directions.append((i, j + 1))

            if not p_directions:
                self.draw_cell(i, j)
                return

            dir_index = random.randrange(len(p_directions))
            direction = p_directions[dir_index]

            # top
            if direction == (i - 1, j):
                current_cell.has_left_wall = False
                self.cells[i - 1][j].has_right_wall = False

            # buttom
            elif direction == (i + 1, j):
                current_cell.has_right_wall = False
                self.cells[i + 1][j].has_left_wall = False

            # left
            elif direction == (i, j - 1):
                current_cell.has_top_wall = False
                self.cells[i][j - 1].has_bottom_wall = False

            # right
            elif direction == (i, j + 1):
                current_cell.has_bottom_wall = False
                self.cells[i][j + 1].has_top_wall = False

            self.break_walls_r(direction[0], direction[1])

    def reset_cells_visited(self):
        for row in self.cells:
            for cell in row:
                cell.visited = False

    def solve(self):
        return self.solve_r(0, 0)

    def solve_r(self, i, j):
        self.animate()
        curr: Cell = self.cells[i][j]
        curr.visited = True
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True
        
        directions = []

        # left
        if i > 0 and not self.cells[i - 1][j].visited:
            directions.append((i - 1, j))

        # right
        if i < self.num_cols - 1 and not self.cells[i + 1][j].visited:
            directions.append((i + 1, j))

        # top
        if j > 0 and not self.cells[i][j - 1].visited:
            directions.append((i, j - 1))

        # buttom
        if j < self.num_rows - 1 and not self.cells[i][j + 1].visited:
            directions.append((i, j + 1))

        for dir in directions:
            # left
            if dir == (i - 1, j):
                if not curr.has_left_wall and not self.cells[i - 1][j].has_right_wall:
                    curr.draw_move(self.cells[dir[0]][dir[1]])
                    val: bool = self.solve_r(dir[0], dir[1])
                    if val:
                        return True
                    curr.draw_move(self.cells[dir[0]][dir[1]], undo=True)

            # right
            elif dir == (i + 1, j):
                if not curr.has_right_wall and not self.cells[i + 1][j].has_left_wall:
                    curr.draw_move(self.cells[dir[0]][dir[1]])
                    val: bool = self.solve_r(dir[0], dir[1])
                    if val:
                        return True
                    curr.draw_move(self.cells[dir[0]][dir[1]], undo=True)

            # top
            elif dir == (i, j - 1):
                if not curr.has_top_wall and not self.cells[i][j - 1].has_bottom_wall:
                    curr.draw_move(self.cells[dir[0]][dir[1]])
                    val: bool = self.solve_r(dir[0], dir[1])
                    if val:
                        return True
                    curr.draw_move(self.cells[dir[0]][dir[1]], undo=True)

            # buttom
            elif dir == (i, j + 1):
                if not curr.has_bottom_wall and not self.cells[i][j + 1].has_top_wall:
                    curr.draw_move(self.cells[dir[0]][dir[1]])
                    val: bool = self.solve_r(dir[0], dir[1])
                    if val:
                        return True
                    curr.draw_move(self.cells[dir[0]][dir[1]], undo=True)
           
        return False