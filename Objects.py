"""
Copyright 2020 Patrick Müller
Tetris
"""
import numpy as np


class Tetromino:

    def __init__(self, tetro_type: str):
        """
        The first element of the self.coords list is always the one in
        the middle except for the o and l one.
        Attributes:
         - self.tetro_type : represents the tetromino
         - self.box_coords : for determining where the tetromino is on
                             the field
         - self.coords     : the inner coordinates, inside the box, used
                             for the rotation with matrix multiplication
        """
        self.tetro_type = tetro_type
        if tetro_type == "o":
            self.box_coords = [(4, 0), (5, 2)]
            self.coords = [np.array([-0.5], [-0.5]), np.array([-0.5], [0.5]),
                           np.array([0.5], [0.5]), np.array([0.5], [-0.5])]
        elif tetro_type == "L":
            self.box_coords = [(3, 0), (5, 3)]
            self.coords = [np.array([0], [0]), np.array([-0.5], [0]),
                           np.array([0.5], [0]), np.array([0.5], [0.5])]
        elif tetro_type == "J":
            self.box_coords = [(3, 0), (5, 3)]
            self.coords = [np.array([0], [0]), np.array([-0.5], [0]),
                           np.array([-0.5], [0.5]), np.array([0.5], [0])]
        elif tetro_type == "z":
            self.box_coords = [(3, 0), (5, 3)]
            self.coords = [np.array([0], [0]), np.array([-0.5], [0.5]),
                           np.array([0], [0.5]), np.array([0.5], [0])]
        elif tetro_type == "s":
            self.box_coords = [(3, 0), (5, 3)]
            self.coords = [np.array([0], [0]), np.array([-0.5], [0]),
                           np.array([0], [0.5]), np.array([0.5], [0.5])]
        elif tetro_type == "T":
            self.box_coords = [(3, 0), (5, 3)]
            self.coords = [np.array([0], [0]), np.array([-0.5], [0]),
                           np.array([0], [0.5]), np.array([0.5], [0])]
        elif tetro_type == "l":
            self.box_coords = [(3, 0), (6, 4)]
            self.coords = [np.array([-1.5], [-0.5]), np.array([-0.5], [-0.5]),
                           np.array([0.5], [-0.5]), np.array([1.5], [-0.5])]

    def rotation(self, direction: bool) -> list:
        """
        The rotation is processed through matrix multiplication.
        The vectors of self.coords are either multiplied with a matrix
        indicating clockwise rotation for direction = True
        and counterclockwise rotation for direction = False

        This function returns a list with the vectors after the
        matrix multiplication. This is needed for checking if the
        rotation was possible and then afterwards applying the
        rotation to the real self.coords
        Basically this is a helper function
        """
        result = []
        clockwise = np.array([0, 1], [-1, 0])
        counterclockwise = np.array([0, -1], [1, 0])

        if direction is True:
            for a in self.coords:
                result = result + [clockwise @ a]
        else:
            for a in self.coords:
                result = result + [counterclockwise @ a]

        return result

    def check_rotation(self, direction: bool):
        """
        This function checks if the rotation was possible,
        with wall kicks and applies them if possible.
        """
        # find out how the rotations work

# make a function that returns the real
# coords of the tiles of a tetromino
# by taking the self.coords and turn
# them into real coords with the self.box_coords
# make a field with dictionary
