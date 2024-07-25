from maze import Maze
from widgets import Window


def main():
    win = Window(800, 600)

    x1 = 5  # starting x position of the maze
    y1 = 5  # starting y position of the maze
    num_rows = 5  # number of rows in the maze
    num_cols = 6  # number of columns in the maze
    cell_size_x = 30  # width of each cell
    cell_size_y = 30  # height of each cell

    # Create and draw the maze
    maze = Maze(x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win)
    maze.create_cells()
    maze.break_entrance_and_exit()
    maze.break_walls_r(2, 2)
    maze.reset_cells_visited()

    win.wait_for_close()


if __name__ == "__main__":
    main()
