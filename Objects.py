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
        self.virtual_coords = None
        if tetro_type == "o":
            self.box_coords = [(4, 0), (5, 1)]
            self.coords = [np.array([[-1], [-1]]), np.array([[-1], [1]]),
                           np.array([[1], [1]]), np.array([[1], [-1]])]
        elif tetro_type == "L":
            self.box_coords = [(3, 0), (5, 2)]
            self.coords = [np.array([[0], [0]]), np.array([[-1], [0]]),
                           np.array([[1], [0]]), np.array([[1], [1]])]
        elif tetro_type == "J":
            self.box_coords = [(3, 0), (5, 2)]
            self.coords = [np.array([[0], [0]]), np.array([[-1], [0]]),
                           np.array([[-1], [1]]), np.array([[1], [0]])]
        elif tetro_type == "z":
            self.box_coords = [(3, 0), (5, 2)]
            self.coords = [np.array([[0], [0]]), np.array([[-1], [1]]),
                           np.array([[0], [1]]), np.array([[1], [0]])]
        elif tetro_type == "s":
            self.box_coords = [(3, 0), (5, 2)]
            self.coords = [np.array([[0], [0]]), np.array([[-1], [0]]),
                           np.array([[0], [1]]), np.array([[1], [1]])]
        elif tetro_type == "T":
            self.box_coords = [(3, 0), (5, 2)]
            self.coords = [np.array([[0], [0]]), np.array([[-1], [0]]),
                           np.array([[0], [1]]), np.array([[1], [0]])]
        elif tetro_type == "l":
            self.box_coords = [(3, 0), (6, 3)]
            self.coords = [np.array([[-2], [1]]), np.array([[-1], [1]]),
                           np.array([[1], [1]]), np.array([[2], [1]])]

    def return_coords(self, virtual: bool) -> list:
        """
        Implement with virtual coords
        Doctest:
        >>> o = Tetromino("o")
        >>> o.return_coords(False)
        [(4, 0), (5, 0), (4, 1), (5, 1)]
        >>> z = Tetromino("z")
        >>> z.return_coords(False)
        [(4, 1), (3, 0), (4, 0), (5, 1)]
        >>> l = Tetromino("l")
        >>> l.return_coords(False)
        [(3, 1), (4, 1), (5, 1), (6, 1)]
        >>> l.box_coords = [(4, 1), (7, 4)]
        >>> l.return_coords(False)
        [(4, 2), (5, 2), (6, 2), (7, 2)]
        """
        if virtual is True:
            co = self.virtual_coords
        else:
            co = self.coords

        result = []
        start_x = self.box_coords[0][0]
        start_y = self.box_coords[0][1]
        coords = []
        for a in co:
            coords = coords + [(a[0][0] + 1, a[1][0] - 1)]

        if self.tetro_type == "o":
            return [self.box_coords[0],
                    (self.box_coords[0][0] + 1, self.box_coords[0][1]),
                    (self.box_coords[0][0], self.box_coords[0][1] + 1),
                    self.box_coords[1]]
        elif self.tetro_type in ("s", "z", "T", "L", "J"):
            for a in coords:
                result = result + [(a[0] + start_x, -1*a[1] + start_y)]
                #                                   --------
                # here we have to invert the a[1] because the self.coords
                # are represented with the normal coordinate system
                # while the self.box_coords have an inverted y axis
            return result
        elif self.tetro_type == "l":
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

    def rotation(self, direction: bool):
        """
        The rotation is processed through matrix multiplication.
        The vectors of self.coords are either multiplied with a matrix
        indicating clockwise rotation for direction = True
        and counterclockwise rotation for direction = False

        This function creates the virtual coords that have to be proven
        by check_rotation()

        Doctests:
        # >>> T = Tetromino("T")
        # >>> T.rotation(True)
        # [[[0], [0]], [[0], [1]], [[1], [0]], [[0], [-1]]]
        # >>> l = Tetromino("l")
        # >>> l.rotation(False)
        # [[[-1], [-2]], [[-1], [-1]], [[-1], [1]], [[-1], [2]]]
        """
        if self.tetro_type == "o":
            return
        result = []
        clockwise = np.array([[0, 1], [-1, 0]])
        counterclockwise = np.array([[0, -1], [1, 0]])

        if direction is True:
            for a in self.coords:
                product = clockwise @ a
                result = result + [product]
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
                product = counterclockwise @ a
                result = result + [product]
                if self.rotation_state == 0:
                    self.rotation_state_virtual = 3
                elif self.rotation_state == 3:
                    self.rotation_state_virtual = 2
                elif self.rotation_state == 2:
                    self.rotation_state_virtual = 1
                elif self.rotation_state == 1:
                    self.rotation_state_virtual = 0

        self.virtual_coords = result

    def check_rotation(self, direction: bool, field: dict):
        """
        This function checks if the rotation was possible,
        with wall kicks and applies them if possible.
        direction = True clockwise
        direction = False counterclockwise
        """
        if self.tetro_type in ("z", "s", "L", "J", "T"):
            if self.rotation_state == 0 and direction is True:
                positions = [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)]
                new_state = 1
            elif self.rotation_state == 1 and direction is False:
                positions = [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)]
                new_state = 0
            elif self.rotation_state == 1 and direction is True:
                positions = [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)]
                new_state = 2
            elif self.rotation_state == 2 and direction is False:
                positions = [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)]
                new_state = 1
            elif self.rotation_state == 2 and direction is True:
                positions = [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]
                new_state = 3
            elif self.rotation_state == 3 and direction is False:
                positions = [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]
                new_state = 2
            elif self.rotation_state == 3 and direction is True:
                positions = [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]
                new_state = 0
            elif self.rotation_state == 0 and direction is False:
                positions = [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]
                new_state = 3

            for new_pos in positions:
                temp = self.box_coords
                # the box coords need to be safed otherwise the new_pos
                # will be added without deleting the old new_pos
                self.box_coords = [(self.box_coords[0][0] + new_pos[0],
                                    self.box_coords[0][1] + new_pos[1]),
                                   (self.box_coords[1][0] + new_pos[0],
                                    self.box_coords[1][1] + new_pos[1])]
                self.rotation(direction)
                new_coords = self.return_coords(True)
                self.box_coords = temp
                for a in new_coords:
                    if field[new_coords] == 1:
                        stop = True
                if stop is True:
                    continue
                else:
                    self.coords = self.virtual_coords
                    self.virtual_coords = None
                    self.rotation_state = new_state

        elif self.tetro_type = "l":
            pass
        # think about how this function wants the virtual coords
        # from rotation() best
        # -----------------------------------------------------
        # needs: - the field and the other tetrominos already placed
        #        - if there is a tetromino -> field[coords] = 1
        #        - virtual coords of the desired rotation
        #        - old and new rotation state
        #        - instructions if a rotation failed (wallkicks)
        # -----------------------------------------------------
        # - checks rotation, remembers old box_coords and if failed then
        #   move the tetromino according to the wallkick data
        # - checks if rotation is possible with the self.virtual_coords
        #   from the method return_coords()
        #   and compares them to the field and if the one self.virtual_coords
        #   is where the field = 1 or its out of the field then the rotation
        #   failed
