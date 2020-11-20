"""
Copyright 2020 Patrick Müller
Tetris - Graphic
"""
from tkinter import *
import time
from Gamelogic import *


class Graphic:
    def __init__(self):
        self.pixel_size = 25
        self.x = 10 * self.pixel_size
        self.y = 20 * self.pixel_size
        self.root = Tk()
        self.root.geometry("1028x720+100+0")
        self.colors = {"L": "orange", "z": "red", "s": "green", "T": "purple",
                       "o": "yellow", "l": "cyan", "J": "blue", "N": "black"}

    def init_canvas(self):
        self.canvas = Canvas(self.root, height=self.y + 25, width=self.x + 15)
        self.canvas.configure(bg="grey")
        for x in range(5, self.x, 26):
            for y in range(5, self.y, 26):
                self.canvas.create_rectangle(x, y, x + 24, y + 24,
                                             fill="black")
        self.canvas.place(x=389, y=20)

    def update_canvas(self, field: dict):
        self.canvas.delete(ALL)
        for x in range(5, self.x, 26):
            for y in range(5, self.y, 26):
                tetri_type = field[((x - 5) // 26, (y - 5) // 26)]
                color = self.colors[tetri_type]
                self.canvas.create_rectangle(x, y, x + 24, y + 24,
                                             fill=color)

    def score_co(self, score, level, lines):
        self.label1 = Label(self.root, text=score + lines,
                            height=100, width=55, bg="grey")
        self.label1.pack(side=LEFT)

    def next_tetrimino(self, tetrimino):
        pass

    def design(self):
        pass


field = {}
for x in range(10):
    for y in range(22):
        field[(x, y)] = "N"
g = Graphic()
g.init_canvas()
g.update_canvas(field)
g.score_co(4, 3, 0)
g.root.mainloop()
