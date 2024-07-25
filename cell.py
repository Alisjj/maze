from widgets import Line, Point, Window


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
        self.visited = False

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
        else:
            self._win.draw_line(left_wall, "#333333")

        if self.has_right_wall:
            self._win.draw_line(right_wall, "white")
        else:
            self._win.draw_line(right_wall, "#333333")

        if self.has_top_wall:
            self._win.draw_line(top_wall, "white")
        else:
            self._win.draw_line(top_wall, "#333333")

        if self.has_bottom_wall:
            self._win.draw_line(bottom_wall, "white")
        else:
            self._win.draw_line(bottom_wall, "#333333")

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
