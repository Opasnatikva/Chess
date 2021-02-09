import string
import pieces


class ChessBoard:
    BOARD_SIZE = 8
    EMPTY_SPACE = chr(12288)
    REPEATS = {pieces.King: 1, pieces.Queen: 1, pieces.Rook: 2, pieces.Bishop: 2, pieces.Knight: 2, pieces.Pawn: 8}
    PIECE_STARTING_LOCATIONS = {pieces.King: (0, "E"), pieces.Queen: (0, "D"), pieces.Rook: (0, "A"),
                                pieces.Bishop: (0, "C"), pieces.Knight: (0, "B"), pieces.Pawn: (1, "A")}

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
        column_names = " " + self.EMPTY_SPACE * 2
        for index in range(self.BOARD_SIZE):
            column_names += string.ascii_uppercase[index] + " " + self.EMPTY_SPACE + " "
        printable_board += column_names + "\n"
        for row_index in range((self.BOARD_SIZE - 1), -1, -1):
            printable_board += str(row_index + 1) + " | "
            for value in self.board[row_index].values():
                printable_board += str(value) + " | "
            printable_board += str(row_index + 1) + "\n"
        printable_board += column_names
        return printable_board

    def initiate_pieces(self):
        for colour in pieces.Colours:
            for piece, number_of_same_pieces in self.REPEATS.items():
                if colour == pieces.Colours.WHITE:
                    row_index = self.PIECE_STARTING_LOCATIONS[piece][0]
                else:
                    row_index = self.BOARD_SIZE - self.PIECE_STARTING_LOCATIONS[piece][0] - 1
                col_index = string.ascii_uppercase.index(self.PIECE_STARTING_LOCATIONS[piece][1])
                for index in range(number_of_same_pieces):
                    if index < 2:
                        col_index += - (col_index * index) + ((self.BOARD_SIZE - col_index - 1) * index)
                    else:
                        col_index -= 1
                    self.board[row_index][string.ascii_uppercase[col_index]] = piece(colour.value)

        # self.board[0]["A"] = pieces.Rook()
        # self.board[0]["E"] = pieces.King()
        # self.board[0]["D"] = pieces.Queen()
        # self.board[0]["C"] = pieces.Bishop()
        # self.board[0]["B"] = pieces.Knight()
        # self.board[1]["A"] = pieces.Pawn()
        # self.board[-1]["A"] = pieces.Rook(pieces.Colours.BLACK.value)
        # self.board[-1]["E"] = pieces.King("black")
        # self.board[-1]["D"] = pieces.Queen("black")
        # self.board[-1]["C"] = pieces.Bishop("black")
        # self.board[-1]["B"] = pieces.Knight("black")
        # self.board[-2]["A"] = pieces.Pawn("black")

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
