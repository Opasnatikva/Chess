import enum

BOARD_SIZE = 8


class Colours(enum.Enum):
    WHITE = "white"
    BLACK = "black"


class WhitePieceNotations(enum.Enum):
    """Unicode characters for the white pieces. The black ones correspond to each of the white ones + 6."""
    KING = 9812
    QUEEN = 9813
    ROOK = 9814
    BISHOP = 9815
    KNIGHT = 9816
    PAWN = 9817
    BLACK_KING = 9818
    BLACK_QUEEN = 9819
    BLACK_ROOK = 9820
    BLACK_BISHOP = 9821
    BLACK_KNIGHT = 9822
    BLACK_PAWN = 9823


class King:
    def __init__(self, colour=Colours.WHITE.value):
        self.colour = colour

    def __str__(self):
        return chr(WhitePieceNotations.KING.value) if self.colour == Colours.WHITE.value else chr(
            WhitePieceNotations.BLACK_KING.value)

    def move_rules(self):
        """The king can move one square in any direction. 8 possible moves generally."""
        coor_deltas = []  # a list of the differences between the original square and the new squares
        for x_change in range(-1, 2):
            for y_change in range(-1, 2):
                new_square = [x_change, y_change]
                if new_square != [0, 0]:
                    coor_deltas.append(new_square)
        return coor_deltas


class Queen:
    def __init__(self, colour=Colours.WHITE.value):
        self.colour = colour

    def __str__(self):
        return chr(WhitePieceNotations.QUEEN.value) if self.colour == Colours.WHITE.value else chr(
            WhitePieceNotations.BLACK_QUEEN.value)

    def move_rules(self):
        coor_deltas = []
        for change in range(-BOARD_SIZE + 1, BOARD_SIZE):
            new_position_horizontal = (0, change)
            new_position_vertical = (change, 0)
            new_position_diagonal = (change, change)
            new_position_diagonal_reverse = (change, -change)
            if new_position_horizontal != (0, 0) and coor_deltas.count(new_position_horizontal) == 0:
                coor_deltas.append(new_position_horizontal)
            if new_position_vertical != (0, 0) and coor_deltas.count(new_position_vertical) == 0:
                coor_deltas.append(new_position_vertical)
            if new_position_diagonal != (0, 0) and coor_deltas.count(new_position_diagonal) == 0:
                coor_deltas.append(new_position_diagonal)
            if new_position_diagonal_reverse != (0, 0) and coor_deltas.count(new_position_diagonal_reverse) == 0:
                coor_deltas.append(new_position_diagonal_reverse)
        return coor_deltas


class Rook:
    def __init__(self, colour=Colours.WHITE.value):
        self.colour = colour

    def __str__(self):
        return chr(WhitePieceNotations.ROOK.value) if self.colour == Colours.WHITE.value else chr(
            WhitePieceNotations.BLACK_ROOK.value)

    def move_rules(self):
        coor_deltas = []
        for change in range(-BOARD_SIZE + 1, BOARD_SIZE):
            new_position_horizontal = (0, change)
            new_position_vertical = (change, 0)
            if new_position_horizontal != (0, 0) and coor_deltas.count(new_position_horizontal) == 0:
                coor_deltas.append(new_position_horizontal)
            if new_position_vertical != (0, 0) and coor_deltas.count(new_position_vertical) == 0:
                coor_deltas.append(new_position_vertical)
        return coor_deltas


class Bishop:
    def __init__(self, colour=Colours.WHITE.value):
        self.colour = colour

    def __str__(self):
        return chr(WhitePieceNotations.BISHOP.value) if self.colour == Colours.WHITE.value else chr(
            WhitePieceNotations.BLACK_BISHOP.value)

    def move_rules(self):
        coor_deltas = []
        for change in range(-BOARD_SIZE + 1, BOARD_SIZE):
            new_position_diagonal = (change, change)
            new_position_diagonal_reverse = (change, -change)
            if new_position_diagonal != (0, 0) and coor_deltas.count(new_position_diagonal) == 0:
                coor_deltas.append(new_position_diagonal)
            if new_position_diagonal_reverse != (0, 0) and coor_deltas.count(new_position_diagonal_reverse) == 0:
                coor_deltas.append(new_position_diagonal_reverse)
        return coor_deltas


class Knight:
    def __init__(self, colour=Colours.WHITE.value):
        self.colour = colour

    def __str__(self):
        return chr(WhitePieceNotations.KNIGHT.value) if self.colour == Colours.WHITE.value else chr(
            WhitePieceNotations.BLACK_KNIGHT.value)

    def move_rules(self):
        delta_one = 1
        delta_two = 2



class Pawn:
    def __init__(self, colour=Colours.WHITE.value):
        self.colour = colour

    def __str__(self):
        return chr(WhitePieceNotations.PAWN.value) if self.colour == Colours.WHITE.value else chr(
            WhitePieceNotations.BLACK_PAWN.value)

    def move_rules(self):
        return [(1, 0), (2, 0), (1, 1), (1, -1)]
