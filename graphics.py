from tkinter import *


class Window:
    def __init__(self, game):
        self.root = Tk()
        self.game = game
        self.start()

    def start(self):
        self.root.bind("<KeyPress>", self.key_listener)
        self.render_grid()

    def end(self):

        self.root.mainloop()

    def render_grid(self, grid=[['-' for i in range(7)] for j in range(6)], x_offset=20, y_offset=20):
        for i in range(8):
            vertical_line = Frame(self.root, bg='white', height=152, width=1)
            vertical_line.place(x=x_offset+20*i, y=y_offset)
        for i in range(6):
            horizontal_line = Frame(self.root, bg='white', height=1, width=140)
            horizontal_line.place(x=x_offset, y=y_offset+26+25*i)

        # grid = [['O' for i in range(7)] for j in range(6)]

        for j in range(6):
            for i in range(7):
                if grid[j][i] != '-':
                    label = Label(self.root, text=grid[j][i])
                    label.place(x=3+x_offset+20*i, y=2 + y_offset + 25*j)

        for i in range(7):
            label = Label(self.root, text=str(i))
            label.place(x=3 + x_offset + 20 * i, y=2 + y_offset + 25 * 6)

    def erase(self):
        blank_frame = Frame(self.root, height=2000, width=2000)
        blank_frame.place(x=0, y=0)

    def key_listener(self, e):
        if e.char == 'p':
            self.game.play_one_turn()
            self.render_grid(self.game.grid)
        if e.char == 'x':
            self.root.destroy()

