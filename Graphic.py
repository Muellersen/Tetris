"""
Copyright 2020 Patrick Müller
Tetris - Graphic
"""
from tkinter import *
import time

from numpy.core.fromnumeric import _swapaxes_dispatcher
from Gamelogic import *
from Objects import *


# todo: comments, movement, rotation
# the gamelogic already has a field and change everything regarding the field
class Graphic:
    def __init__(self, game: GameLogic):
        self.pixel_size = 25
        self.x = 10 * self.pixel_size
        self.y = 20 * self.pixel_size
        self.root = Tk()
        self.root.geometry("1028x720+100+0")
        self.colors = {"L": "orange", "z": "red", "s": "green", "T": "purple",
                       "o": "yellow", "l": "cyan", "J": "blue", "N": "black"}
        # self.field = {}  # not needed delete pls
        # for x in range(10):
        #     for y in range(22):
        #         self.field[(x, y)] = "N"
        self.game = GameLogic()

    def init_canvas(self):
        self.canvas = Canvas(self.root, height=self.y + 25, width=self.x + 15)
        self.canvas.configure(bg="grey")
        for x in range(5, self.x, 26):
            for y in range(5, self.y, 26):
                self.canvas.create_rectangle(x, y, x + 24, y + 24,
                                             fill="black")
        self.canvas.place(x=389, y=20)

    def update_canvas(self):
        self.canvas.delete(ALL)
        for x in range(5, self.x, 26):
            for y in range(5, self.y, 26):
                tetri_type = self.game.field[((x - 5) // 26, (y - 5) // 26)]
                color = self.colors[tetri_type]
                self.canvas.create_rectangle(x, y, x + 24, y + 24,
                                             fill=color)

    def score_co(self, score, level, lines):
        self.label1 = Label(self.root, text=score + lines,
                            height=100, width=55, bg="grey")
        self.label1.pack(side=LEFT)

    def next_tetrimino(self, tetrimino):
        self.game.spawn_tetrimino()
        current_tetrimino = self.game.current_tetrimino
        tetrimino_coords = current_tetrimino.return_coords(False)
        for coord in tetrimino_coords:
            self.game.field[(coord[0], coord[1])] = current_tetrimino.tetro_type

    def apply_gravity(self):
        current_tetrimino = self.game.current_tetrimino
        tetrimino_coords = current_tetrimino.return_coords(False)
        for coord in tetrimino_coords:
            self.game.field[(coord[0], coord[1])] = "N"
        self.game.move_down()
        tetrimino_coords = current_tetrimino.return_coords(False)
        for coord in tetrimino_coords:
            self.game.field[(coord[0], coord[1])] = current_tetrimino.tetro_type

    def load_design(self):
        pass


g = Graphic()
g.init_canvas()
g.update_canvas()
g.next_tetrimino("")
g.score_co(4, 3, 0)
# for x in range(6):
#     g.gravity()
#     g.update_canvas()
#     g.root.update_idletasks()
#     g.root.update()
#     time.sleep(0.5)
# g.next_tetrimino("")
# for x in range(6):
#     g.gravity()
#     g.update_canvas()
#     g.root.update_idletasks()
#     g.root.update()
#     time.sleep(0.5)
while(True):
    g.apply_gravity()
    g.update_canvas()
    g.root.update_idletasks()
    g.root.update()
    time.sleep(0.3)
# g.root.mainloop()
