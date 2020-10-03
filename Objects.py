"""
Copyright 2020 Patrick Müller
Tetris
"""
import numpy as np


class Object:
    """
    The superclass for the blocks in Tetris
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def rotate(self, vectors: list):
        """
        The vectors are representing the squares of a tetris object.
        The vectors are pointing to the top left corner of the squares,
        which make up a whole tetris object.
        The matrix represents a 90 degree rotation clockwise or
        mathematically negativ rotation.
        [ 0, 1]
        [-1, 0]
        """
        rotation_matrix = np.array([0, 1], [-1, 0])
        for a in range(len(vectors)):
            vectors[a] = rotation_matrix @ vectors[a]

    def move_right(self):
        self.x = self.x + 1

    def move_left(self):
        self.x = self.x - 1

    def move_down(self):
        self.y = self.y + 1


class Tetriminoes(Object):

    def __init__(self, x: int, y: int, block_type: int):
        super().__init__(x, y)
        if block_type == 0:
            # the o
            self.vectors = [(0, 0), (-1, 0), (-1, 1), (0, 1)]
        elif block_type == 1:
            # the z
            self.vectors = [(0, 0), (-1, 1), (0, 1), (1, 0)]
        elif block_type == 2:
            # the s
            self.vectors = [(0, 0), (-1, 0), (0, 1), (1, 1)]
        elif block_type == 3:
            # the L
            self.vectors = [(0, 0), (-1, 0), (1, 1), (1, 0)]
        elif block_type == 4:
            # the j
            self.vectors = [(0, 0), (-1, 0), (-1, 1), (1, 0)]
        elif block_type == 5:
            # the T
            self.vectors = [(0, 0), (-1, 0), (0, 1), (1, 0)]
        elif block_type == 6:
            # the l
            self.vectors = [(-1.5, -0.5), (-0.5, -0.5),
                            (0.5, -0.5), (1.5, -0.5)]
