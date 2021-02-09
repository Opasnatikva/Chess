import enum


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


class King:
    def __init__(self, colour=Colours.WHITE.value):
        self.colour = colour

    def __str__(self):
        return "K"

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
        return WhitePieceNotations.QUEEN.value


class Rook:
    def __init__(self, colour=Colours.WHITE.value):
        self.colour = colour

    def __str__(self):
        return WhitePieceNotations.ROOK.value


class Bishop:
    def __init__(self, colour=Colours.WHITE.value):
        self.colour = colour

    def __str__(self):
        return WhitePieceNotations.BISHOP.value


class Knight:
    def __init__(self, colour=Colours.WHITE.value):
        self.colour = colour

    def __str__(self):
        return WhitePieceNotations.KNIGHT.value


class Pawn:
    def __init__(self, colour=Colours.WHITE.value):
        self.colour = colour

    def __str__(self):
        return WhitePieceNotations.PAWN.value
