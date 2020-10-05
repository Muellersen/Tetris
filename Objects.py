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
         - self.rotation_state: 0 = How they are spawned
                                1 = one clockwise rotation from spawn
                                2 = two clockwise or counterclockwise
                                    roations from spawn
                                3 = one counterclockwise roation
        """
        self.tetro_type = tetro_type
        self.rotation_state = 0
        self.rotation_state_virtual = 0
        if tetro_type == "o":
            self.box_coords = [(4, 0), (5, 2)]
            self.coords = [np.array([-1], [-1]), np.array([-1], [1]),
                           np.array([1], [1]), np.array([1], [-1])]
        elif tetro_type == "L":
            self.box_coords = [(3, 0), (5, 3)]
            self.coords = [np.array([0], [0]), np.array([-1], [0]),
                           np.array([1], [0]), np.array([1], [1])]
        elif tetro_type == "J":
            self.box_coords = [(3, 0), (5, 3)]
            self.coords = [np.array([0], [0]), np.array([-1], [0]),
                           np.array([-1], [1]), np.array([1], [0])]
        elif tetro_type == "z":
            self.box_coords = [(3, 0), (5, 3)]
            self.coords = [np.array([0], [0]), np.array([-1], [1]),
                           np.array([0], [1]), np.array([1], [0])]
        elif tetro_type == "s":
            self.box_coords = [(3, 0), (5, 3)]
            self.coords = [np.array([0], [0]), np.array([-1], [0]),
                           np.array([0], [1]), np.array([1], [1])]
        elif tetro_type == "T":
            self.box_coords = [(3, 0), (5, 3)]
            self.coords = [np.array([0], [0]), np.array([-1], [0]),
                           np.array([0], [1]), np.array([1], [0])]
        elif tetro_type == "l":
            self.box_coords = [(3, 0), (6, 4)]
            self.coords = [np.array([-2], [1]), np.array([-1], [1]),
                           np.array([1], [1]), np.array([2], [1])]

    def return_coords(self) -> list:
        result = []
        start_x = self.box_coords[0][0]
        start_y = self.box_coords[0][1]

        for a in self.coords:
            coords = coords + [(a[0] + 1, a[1] - 1)]

        if x == 2 and y == 2:
            return [self.box_coords[0],
                    (self.box_coords[0][0] + 1, self.box_coords[0][1]),
                    (self.box_coords[0][0], self.box_coords[0][1] + 1),
                    self.box_coords[1]]
        elif x == 3 and y == 3:
            for a in coords:
                result = result + [(a[0] + start_x, -1*a[1] + start_y)]
                #                                   --------
                # here we have to invert the a[1] because the self.coords
                # are represented with the normal coordinate system
                # while the self.box_coords have an inverted y axis
                return result
        elif x == 4 and y == 4:
            # here we only need to find out one value of the "l"
            # in order to find out every other values
            # so there are 4 possibilities for each rotation_state
            if self.rotation_state == 0:
                result = [(start_x + a, start_y + 1) for a in range(4)]
                return result
            elif self.rotation_state == 1:
                result = [(start_x + 2, start_y + a) for a in range(4)]
                return result
            elif self.rotation_state == 2:
                result = [(start_x + a, start_y + 2) for a in range(4)]
                return result
            elif self.rotation_state == 3:
                result = [(start_x + 1, start_y + a) for a in range(4)]
                return result

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
                if self.rotation_state == 0:
                    self.rotation_state_virtual = 1
                elif self.rotation_state == 1:
                    self.rotation_state_virtual = 2
                elif self.rotation_state == 2:
                    self.rotation_state_virtual = 3
                elif self.rotation_state == 3:
                    self.rotation_state_virtual = 0
        else:
            for a in self.coords:
                result = result + [counterclockwise @ a]
                if self.rotation_state == 0:
                    self.rotation_state_virtual = 3
                elif self.rotation_state == 3:
                    self.rotation_state_virtual = 2
                elif self.rotation_state == 2:
                    self.rotation_state_virtual = 1
                elif self.rotation_state == 1:
                    self.rotation_state_virtual = 0

        return result

    def check_rotation(self, direction: bool, field: dict):
        """
        This function checks if the rotation was possible,
        with wall kicks and applies them if possible.
        """


# make a function that returns the real
# coords of the tiles of a tetromino
# by taking the self.coords and turn
# them into real coords with the self.box_coords
# make a field with dictionary
# track the state of the rotation
