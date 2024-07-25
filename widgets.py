from tkinter import Tk, Canvas


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
