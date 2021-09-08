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
    def __init__(self, game: GameLogic, state: int):
        self.pixel_size = 25
        self.x = 10 * self.pixel_size
        self.y = 20 * self.pixel_size
        self.state = state
        self.root = Tk()
        self.root.geometry("1028x720+100+0")
        self.colors = {"L": "orange", "z": "red", "s": "green", "T": "purple",
                       "o": "yellow", "l": "cyan", "J": "blue", "N": "black"}
        self.game = game

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
                tetri_type = self.game.field[((x - 5) // 26, ((y - 5) // 26) + 2)]
                color = self.colors[tetri_type]
                self.canvas.create_rectangle(x, y, x + 24, y + 24,
                                             fill=color)

    def init_score(self):
        self.label1 = Label(self.root, text=0,
                            height=100, width=55, bg="grey")
        self.label1.pack(side=LEFT)

    def update_score(self):
        self.label1['text'] = self.game.score

    def next_tetrimino(self):
        self.game.spawn_tetrimino()
        current_tetrimino = self.game.current_tetrimino
        tetrimino_coords = current_tetrimino.return_coords(False)
        for coord in tetrimino_coords:
            self.game.field[(coord[0], coord[1])] = current_tetrimino.tetro_type

    def event_handler(self, event):
        self.root.unbind("<Up>")
        self.root.unbind("<Left>")
        self.root.unbind("<Right>")
        self.root.unbind("<Down>")
        self.root.unbind("<space>")
        self.root.unbind("x")
        key = event.keysym
        if key == "Up":
            self.game.rotate_right()
        elif key == "Down":
            self.game.soft_drop()
        elif key == "x":
            self.game.rotate_left()
        elif key == "Right":
            self.game.move_right()
        elif key == "Left":
            self.game.move_left()
        elif key == "space":
            self.game.hard_drop()
        elif key == "Escape":
            if self.state == 2:
                self.state = -1
            else:
                self.state = 2
        self.root.bind("<Up>", self.event_handler)
        self.root.bind("x", self.event_handler)
        self.root.bind("<Right>", self.event_handler)
        self.root.bind("<Left>", self.event_handler)
        self.root.bind("<Down>", self.event_handler)
        self.root.bind("<space>", self.event_handler)
        # make function to pause the game
        # self.update_canvas()
        # self.root.update_idletasks()
        # self.root.update()

    def load_start_menu(self):
        pass

    def load_pause_menu(self):
        pass
