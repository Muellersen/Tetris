"""
Copyright 2020 Patrick Müller
Tetris
"""
from Objects import *
import random

# field 10x22
# if check_rotation is True -> get coords
# and field[coords] = "Tetrimino letter"
# score function
# showing the next Tetrimino
# level
# acceleration of the gravity


class GameLogic:

    def __init__(self):
        self.field = {}
        for x in range(10):
            for y in range(22):
                self.field[(x, y)] = "N"
        self.score = 0
        self.level = 0
        self.tetrimino_list = ["L", "J", "z", "s", "T", "l", "o"]
        self.list_pointer = 0
        self.current_tetrimino = None
        self.next_tetrimino = None

    def shuffle_tetriminos(self) -> list:
        random.shuffle(self.tetrimino_list)

    def line_is_full(self):
        lines = 0
        for y in range(2, 22, 1):
            count = 0
            for x in range(10):
                if self.field[(x, y)] in ["L", "J", "z", "s", "T", "l", "o"]:
                    count += 1
            if count == 10:
                for x in range(10):
                    self.field[(x, y)] = "N"
                lines += 1
        if lines == 0:
            return
        elif lines == 1:
            self.score = self.score + 40*(self.level + 1)
        elif lines == 2:
            self.score = self.score + 100*(self.level + 1)
        elif lines == 3:
            self.score = self.score + 300*(self.level + 1)
        elif lines == 4:
            self.score = self.score + 1200*(self.level + 1)

    def get_gravity(self):
        if self.level == 0:
            return 1
        else:
            return 1 - self.level / 10

    def spawn_tetrimino(self):
        self.current_tetrimino = Tetrimino(tetrimino_list[list_pointer])
        if list_pointer + 1 < len(tetrimino_list):
            self.next_tetrimino = tetrimino_list[list_pointer + 1]
            list_pointer += 1
        else:
            self.shuffle_tetriminos
            list_pointer = 0
            self.next_tetrimino = tetrimino_list[list_pointer]

    def move(self, direction: bool):
        self.current_tetrimino.move(direction, self.field)

    def move_down(self) -> bool:
        if self.current_tetrimino.check_collision(self.field) is True:
            coords = self.current_tetrimino.return_coords(False)
            letter = self.current_tetrimino.tetro_type
            for a in coords:
                field[a] = letter
            return False
        else:
            self.current_tetrimino.fall()

    def coords(self):
        return self.current_tetrimino.return_coords(False)

    def soft_drop(self):
        pass

    def hard_drop(self):
        pass

    def is_lost(self) -> bool:
        pass
