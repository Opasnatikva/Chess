import string
import pieces


class ChessBoard:
    BOARD_SIZE = 8
    EMPTY_SPACE = " "
    REPEATS = {pieces.King: 1, pieces.Queen: 1, pieces.Rook: 2, pieces.Bishop: 2, pieces.Knight: 2, pieces.Pawn: 8}
    PIECE_STARTING_LOCATIONS = {pieces.King: (1, "E"), pieces.Queen: (1, "D"), pieces.Rook: (1, "A"),
                                pieces.Bishop: (1, "C"), pieces.Knight: (1, "B"), pieces.Pawn: (2, "A")}

    def __init__(self):
        self.generate_board()
        self.initiate_pieces()

    def generate_board(self):
        self.board = [{string.ascii_uppercase[index]: self.EMPTY_SPACE for index in range(self.BOARD_SIZE)} for _ in
                      range(self.BOARD_SIZE)[::-1]]
        # self.board = {string.ascii_uppercase[x]: [self.EMPTY_SPACE for _ in range(self.BOARD_SIZE)] for x in
        #               range(self.BOARD_SIZE)[::-1]}

    def __call__(self):
        pass

    def __str__(self):
        printable_board = ""
        column_names = "    "
        for index in range(self.BOARD_SIZE):
            column_names += string.ascii_uppercase[index] + "   "
        printable_board += column_names + "\n"
        for row_index in range(len(self.board)):
            printable_board += str(self.BOARD_SIZE - row_index) + " | "
            for value in self.board[row_index].values():
                printable_board += value + " | "
            printable_board += str(self.BOARD_SIZE - row_index) + "\n"
        printable_board += column_names
        return printable_board

    def initiate_pieces(self):
        for piece in self.REPEATS.keys():
            for colour in pieces.Colours:
                    self.board[self.PIECE_STARTING_LOCATIONS[str(piece)]][
                        self.PIECE_STARTING_LOCATIONS[str(piece)] = piece(colour)
        pass

    # self.white_king = King("white")
    # self.black_king = King("black")
    # piece_names = {}
    # for name, member in list(WhitePieceNotations.__members__.items()):
    #     print(chr(member.value))
    # print("")
    # for name, member in list(WhitePieceNotations.__members__.items()):
    #     print(chr(member.value + 6))
    # # self.board[self.element.initial_coordinates[0]][self.element.initial_coordinates[1]] = self.element
    # # self.board[self.white_king.initial_coordinates[0]][self.white_king.initial_coordinates[1]] = self.white_king
    # # self.board[self.black_king.initial_coordinates[0]][self.black_king.initial_coordinates[1]] = self.black_king
    # return piece_names


if __name__ == "__main__":
    board_instance = ChessBoard()
    print(board_instance)
