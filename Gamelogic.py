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
        self.level_counter = 0
        self.tetrimino_list = ["L", "J", "z", "s", "T", "l", "o"]
        self.list_pointer = 0
        self.current_tetrimino = None
        self.next_tetrimino = None

    def shuffle_tetriminos(self) -> list:
        """
        Shuffles the tetrimino_list randomly. With this,
        it is made sure that there wont be the same tetrimino
        over and over again.
        """
        random.shuffle(self.tetrimino_list)

    def line_is_full(self):
        """
        This function counts the amount of
        lines which are full, deletes them and
        increases the score. This function also lets the remaining
        tetriminos above fall down.
        Increases the level if 10 lines were cleared
        """
        lines = 0
        highest_line = 0
        for y in range(2, 22, 1):
            count = 0
            for x in range(10):
                if self.field[(x, y)] in ["L", "J", "z", "s", "T", "l", "o"]:
                    count += 1
            if count == 10:
                if y > highest_line:
                    highest_line = y
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

        self.level_counter += lines
        if self.level_counter >= 10:
            self.level += 1
            self.level_counter = self.level_counter % 10

        for y in range(highest_line, 0, 1):
            # goes the opposite way because otherwise the
            # order of the tetriminos will be wrong
            for x in range(10):
                if field[(x, y)] in self.tetrimino_list:
                    y2 = y
                    while True:
                        if (field[(x, y2 + 1)] not in self.tetrimino_list
                           or field.get(x, y2 + 1) is not None):
                            y2 += 1
                        else:
                            break
                    field[(x, y2)] = field[(x, y)]

    def get_gravity(self):
        """
        Returns the gravity according to the level.

        !!! Think about the numbers !!!
        1 - self.level / 10
        1 - 10 / 10 = 0 ???
        """
        if self.level == 0:
            return 1
        else:
            return 1 - self.level / 31

    def spawn_tetrimino(self):
        """
        This function spawns a Tetrimino and already
        sets the next tetrimino with the tetrimino_list
        if the current tetrimino is the last element in the
        tetrimino_list, the list will be shuffled and
        the next_tetrimino will be the first element of
        the shuffled list.
        """
        self.current_tetrimino = Tetrimino(tetrimino_list[list_pointer])
        if list_pointer + 1 < len(tetrimino_list):
            self.next_tetrimino = tetrimino_list[list_pointer + 1]
            list_pointer += 1
        else:
            self.shuffle_tetriminos()
            list_pointer = 0
            self.next_tetrimino = tetrimino_list[list_pointer]

    def move(self, direction: bool):
        """
        This function calls the function Tetrimino.move()
        from the Tetrimino class in Objects.py
        """
        self.current_tetrimino.move(direction, self.field)

    def move_down(self) -> bool:
        """
        This function checks if the tetrimino can be moved downwards
        without colliding. If there is no collision, the tetrimino will
        be locked in.
        """
        if self.current_tetrimino.check_collision(self.field) is True:
            coords = self.current_tetrimino.return_coords(False)
            letter = self.current_tetrimino.tetro_type
            for a in coords:
                field[a] = letter
            return False
        else:
            self.current_tetrimino.fall()

    def coords(self):
        """
        Returns the coordinates of the current tetrimino
        which the player can control.
        """
        return self.current_tetrimino.return_coords(False)

    def soft_drop(self):
        """
        This function moves the tetrimino one line downwards
        and adds 1 points per line.
        This function needs to be called more often as the
        tetrimino should fall down faster.
        """
        self.move_down()
        self.score += 1

    def hard_drop(self):
        """
        This function moves the tetrimino one line downwards
        and adds 2 points per line.
        This function needs to be called multiple times in
        a short period of time so it looks like
        it falls down instantly
        """
        self.move_down()
        self.score += 2

    def is_lost(self) -> bool:
        """
        Checks the line above the playground.
        If there is a tetrimino locked (field[coords] in self.tetrimino_list)
        it returns True else it will return False
        """
        for x in range(10):
            if self.field[(x, 1)] == 1:
                return True
        return False
