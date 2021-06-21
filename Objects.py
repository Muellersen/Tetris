"""
Copyright 2020 Patrick Müller
Tetris
"""
import numpy as np


class Tetrimino:

    def __init__(self, tetro_type: str):
        """
        The first element of the self.coords list is always the one in
        the middle except for the o and l one.
        Attributes:
         - self.tetro_type : represents the Tetrimino
         - self.box_coords : for determining where the Tetrimino is on
                             the field
         - self.coords     : the inner coordinates, inside the box, used
                             for the rotation with matrix multiplication
         - self.rotation_state: 0 = How they are spawned
                                1 = one clockwise rotation from spawn
                                2 = two clockwise or counterclockwise
                                    roations from spawn
                                3 = one counterclockwise roation
        """
        self.tetrimino_tuple = ("L", "J", "z", "s", "T", "l", "o")
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
        >>> o = Tetrimino("o")
        >>> o.return_coords(False)
        [(4, 0), (5, 0), (4, 1), (5, 1)]
        >>> z = Tetrimino("z")
        >>> z.return_coords(False)
        [(4, 1), (3, 0), (4, 0), (5, 1)]
        >>> l = Tetrimino("l")
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
        >>> T = Tetrimino("T")
        >>> T.rotation(True)
        >>> T.virtual_coords
        [array([[0],
               [0]]), array([[0],
               [1]]), array([[1],
               [0]]), array([[ 0],
               [-1]])]
        >>> T.rotation(False)
        >>> T.virtual_coords
        [array([[0],
               [0]]), array([[ 0],
               [-1]]), array([[-1],
               [ 0]]), array([[0],
               [1]])]
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

        -----------------------------------------------------
        needs:  - the field and the other Tetriminos already placed
                - if there is a Tetrimino -> field[coords] in
                  self.tetrimino_tuple
                - virtual coords of the desired rotation
                - old and new rotation state
                - instructions if a rotation failed (wallkicks)
        -----------------------------------------------------
           checks rotation, remembers old box_coords and if failed then
           move the Tetrimino according to the wallkick data
         - checks if rotation is possible with the self.virtual_coords
           from the method return_coords()
           and compares them to the field and if the one self.virtual_coords
           is where the field = "tetrimino Letter"
           or its out of the field then the rotation
           failed

        Doctests:
        >>> T = Tetrimino("T")
        >>> field = {}
        >>> coord = [(a, b) for a in range(10) for b in range(23)]
        >>> for a in coord: field[a] = "N"
        >>> T.check_rotation(True, field)
        >>> T.rotation_state == 1
        True
        >>> T.coords
        [array([[0],
               [0]]), array([[0],
               [1]]), array([[1],
               [0]]), array([[ 0],
               [-1]])]
        """
        box = self.box_coords
        if self.tetro_type in ("z", "s", "L", "J", "T"):
            if self.rotation_state == 0 and direction is True:
                # 0 -> 1
                positions = [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)]
                new_state = 1
            elif self.rotation_state == 1 and direction is False:
                # 1 -> 0
                positions = [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)]
                new_state = 0
            elif self.rotation_state == 1 and direction is True:
                # 1 -> 2
                positions = [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)]
                new_state = 2
            elif self.rotation_state == 2 and direction is False:
                # 2 -> 1
                positions = [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)]
                new_state = 1
            elif self.rotation_state == 2 and direction is True:
                # 2 -> 3
                positions = [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]
                new_state = 3
            elif self.rotation_state == 3 and direction is False:
                # 3 -> 2
                positions = [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]
                new_state = 2
            elif self.rotation_state == 3 and direction is True:
                # 3 -> 0
                positions = [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]
                new_state = 0
            elif self.rotation_state == 0 and direction is False:
                # 0 -> 3
                positions = [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]
                new_state = 3

            for new_pos in positions:
                # here each position will be checked if a rotation
                # fails because there is an obstacle
                temp = self.box_coords
                # the box coords need to be safed otherwise the new_pos
                # will be added without deleting the old new_pos
                stop = False
                self.box_coords = [(self.box_coords[0][0] + new_pos[0],
                                    self.box_coords[0][1] + new_pos[1]),
                                   (self.box_coords[1][0] + new_pos[0],
                                    self.box_coords[1][1] + new_pos[1])]
                self.rotation(direction)
                new_coords = self.return_coords(True)  # new virtual coords
                for a in new_coords:  # checking if the Tetrimino hit smth
                    if (field.get(a) is None
                       or field[a] in self.tetrimino_tuple):
                        # the first condition is for checking if the
                        # Tetrimino hit another Tetrimino lying there
                        # the second for checking if its outside of the field
                        stop = True
                if stop is True:
                    # if the rotation didnt work we have to
                    # put Tetrimino back at his previous position
                    # so the next position can be tested or
                    # it will stay in place
                    self.box_coords = temp
                    continue
                else:
                    self.coords = self.virtual_coords  # applied new coords
                    self.virtual_coords = None
                    self.rotation_state = new_state
                    break

        elif self.tetro_type == "l":
            if self.rotation_state == 0 and direction is True:
                # 0 -> 1
                positions = [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)]
                new_state = 1
            elif self.rotation_state == 1 and direction is False:
                # 1 -> 0
                positions = [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)]
                new_state = 0
            elif self.rotation_state == 1 and direction is True:
                # 1 -> 2
                positions = [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)]
                new_state = 2
            elif self.rotation_state == 2 and direction is False:
                # 2 -> 1
                positions = [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)]
                new_state = 1
            elif self.rotation_state == 2 and direction is True:
                # 2 -> 3
                positions = [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)]
                new_state = 3
            elif self.rotation_state == 3 and direction is False:
                # 3 -> 2
                positions = [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)]
                new_state = 2
            elif self.rotation_state == 3 and direction is True:
                # 3 -> 0
                positions = [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)]
                new_state = 0
            elif self.rotation_state == 0 and direction is False:
                # 0 -> 3
                positions = [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)]
                new_state = 3

            for new_pos in positions:
                # here each position will be checked if a rotation
                # fails because there is an obstacle
                temp = self.box_coords
                # the box coords need to be safed otherwise the new_pos
                # will be added without deleting the old new_pos
                stop = False
                self.box_coords = [(self.box_coords[0][0] + new_pos[0],
                                    self.box_coords[0][1] + new_pos[1]),
                                   (self.box_coords[1][0] + new_pos[0],
                                    self.box_coords[1][1] + new_pos[1])]
                self.rotation(direction)
                new_coords = self.return_coords(True)  # new virtual coords
                for a in new_coords:  # checking if the Tetrimino hit smth
                    if (field.get(a) is None
                       or field[a] in self.tetrimino_tuple):
                        stop = True
                if stop is True:
                    # if the rotation didnt work we have to
                    # put Tetrimino back at his previous position
                    # so the next position can be tested or
                    # it will stay in place
                    self.box_coords = temp
                    continue
                else:
                    self.coords = self.virtual_coords  # applied new coords
                    self.virtual_coords = None
                    self.rotation_state = new_state
                    break

    def move(self, direction: bool, field: dict):
        """
        This function takes a direction (right - True, left - False)
        and a field, a dictionary and checks, if the movement is
        possible. The movement is not possible if the coords are not
        in the field or another Tetrimino is in the way

        Doctest:
        >>> T = Tetrimino("T")
        >>> field = {}
        >>> coord = [(a, b) for a in range(10) for b in range(23)]
        >>> for a in coord: field[a] = "N"
        >>> field[(6, 1)] = "L"
        >>> T.move(True, field)
        >>> T.box_coords == [(3, 0), (5, 2)]
        True
        >>> T.move(False, field)
        >>> T.box_coords == [(2, 0), (4, 2)]
        True
        """
        current_coords = self.return_coords(False)
        if direction is True:
            for coord in current_coords:
                
                if (coord[0] + 1, coord[1]) in current_coords:
                    continue
                if (field.get((coord[0] + 1, coord[1])) is None
                   or field[(coord[0] + 1, coord[1])] in self.tetrimino_tuple):
                    return
            self.box_coords = [(self.box_coords[0][0] + 1,
                                self.box_coords[0][1]),
                               (self.box_coords[1][0] + 1,
                                self.box_coords[1][1])]
        else:
            for coord in current_coords:
                if (coord[0] - 1, coord[1]) in current_coords:
                    continue
                if (field.get((coord[0] - 1, coord[1])) is None
                   or field[(coord[0] - 1, coord[1])] in self.tetrimino_tuple):
                    return
            self.box_coords = [(self.box_coords[0][0] - 1,
                                self.box_coords[0][1]),
                               (self.box_coords[1][0] - 1,
                                self.box_coords[1][1])]

    def fall(self):
        """
        This function lets the Tetrimino move down.
        """
        self.box_coords = [(self.box_coords[0][0],
                            self.box_coords[0][1] + 1),
                           (self.box_coords[1][0],
                            self.box_coords[1][1] + 1)]

    def check_collision(self, field: dict) -> bool:
        """
        Here we have to check the surroundings, so a collision
        means the Tetriminoes touch each other.
        This function checks the collision under the Tetrimino
        True - collision detected
        False - no collision

        Doctest:
        >>> T = Tetrimino("T")
        >>> field = {}
        >>> coord = [(a, b) for a in range(10) for b in range(23)]
        >>> for a in coord: field[a] = "N"
        >>> field[(3, 2)] = "L"
        >>> T.check_collision(field)
        True
        >>> field[(3, 2)] = "N"
        >>> T.check_collision(field)
        False
        """
        # tetriminos collide with themselves
        current_coords = self.return_coords(False)
        for coord in current_coords:
            if ((field.get((coord[0], coord[1] + 1)) == "X"
               or field[(coord[0], coord[1] + 1)] in self.tetrimino_tuple)
               and (coord[0], coord[1] + 1) not in current_coords):
                return True
        return False
