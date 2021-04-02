import enum

BOARD_SIZE = 8


def move_rules_rook():
    coor_deltas = [[], [], [], []]
    for delta in range(1, BOARD_SIZE):
        delta_up = (delta, 0)
        delta_down = (-delta, 0)
        delta_left = (0, -delta)
        delta_right = (0, delta)
        coor_deltas[0].append(delta_left)
        coor_deltas[1].append(delta_up)
        coor_deltas[2].append(delta_right)
        coor_deltas[3].append(delta_down)
    return coor_deltas


def move_rules_bishop():
    coor_deltas = [[], [], [], []]
    for delta in range(1, BOARD_SIZE):
        delta_up_right = (delta, delta)
        delta_down_right = (-delta, delta)
        delta_up_left = (delta, -delta)
        delta_down_left = (-delta, -delta)
        coor_deltas[0].append(delta_up_right)
        coor_deltas[1].append(delta_down_right)
        coor_deltas[2].append(delta_up_left)
        coor_deltas[3].append(delta_down_left)
    return coor_deltas


class colors(enum.Enum):
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
    moved = False
    left_right_castles = [[0, -2], [0, 2]]

    def __init__(self, color=colors.WHITE.value):
        self.color = color

    def __str__(self):
        return chr(WhitePieceNotations.KING.value) if self.color == colors.WHITE.value else chr(
            WhitePieceNotations.BLACK_KING.value)

    @property
    def move_rules(self):
        """The king can move one square in any direction. 8 possible moves generally."""

        coor_deltas = []  # a list of the differences between the original square and the new squares
        for x_change in range(-1, 2):
            for y_change in range(-1, 2):
                new_square = [[x_change, y_change]]
                if new_square != [0, 0]:
                    coor_deltas.append(new_square)
        if not self.moved:
            coor_deltas[3].append(self.left_right_castles[0])
            coor_deltas[5].append(self.left_right_castles[1])
        return coor_deltas


class Queen:
    def __init__(self, color=colors.WHITE.value):
        self.color = color
        coor_deltas = move_rules_rook()
        coor_deltas.extend(move_rules_bishop())
        self.move_rules = coor_deltas

    def __str__(self):
        return chr(WhitePieceNotations.QUEEN.value) if self.color == colors.WHITE.value else chr(
            WhitePieceNotations.BLACK_QUEEN.value)


class Rook:
    moved = False
    castle_moves = [(0, 3), (0, -2)]

    def __init__(self, color=colors.WHITE.value):
        self.color = color
        self.move_rules = move_rules_rook()

    def __str__(self):
        return chr(WhitePieceNotations.ROOK.value) if self.color == colors.WHITE.value else chr(
            WhitePieceNotations.BLACK_ROOK.value)


class Bishop:
    def __init__(self, color=colors.WHITE.value):
        self.color = color
        self.move_rules = move_rules_bishop()

    def __str__(self):
        return chr(WhitePieceNotations.BISHOP.value) if self.color == colors.WHITE.value else chr(
            WhitePieceNotations.BLACK_BISHOP.value)


class Knight:
    move_rules = [[(-1, 2)], [(-2, 1)], [(1, 2)], [(2, 1)], [(1, -2)], [(2, -1)], [(-1, -2)], [(-2, -1)]]

    def __init__(self, color=colors.WHITE.value):
        self.color = color

    def __str__(self):
        return chr(WhitePieceNotations.KNIGHT.value) if self.color == colors.WHITE.value else chr(
            WhitePieceNotations.BLACK_KNIGHT.value)


class Pawn:
    forward_move_rule = [(1, 0)]
    double_move_rule = [(2, 0)]
    take_rules = [[(1, -1)], [(1, 1)]]
    transformations = {
        'Q': Queen(),
        'R': Rook(),
        'B': Bishop(),
        'N': Knight()
    }

    def __init__(self, color=colors.WHITE.value):
        self.color = color

    def __str__(self):
        return chr(WhitePieceNotations.PAWN.value) if self.color == colors.WHITE.value else chr(
            WhitePieceNotations.BLACK_PAWN.value)

    def choose_pawn_transformation(self):
        while True:
            transformation = input("'Q' for Queen, 'R' for Rook, 'B' for Bishop, 'N' for Knight.").upper()
            if transformation in self.transformations.keys():
                break
        return self.transformations[transformation]
