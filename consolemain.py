import string
import pieces


class ChessBoard:
    BOARD_SIZE = 8
    EMPTY_SPACE = chr(12288)
    REPEATS = {pieces.King: 1, pieces.Queen: 1, pieces.Rook: 2, pieces.Bishop: 2, pieces.Knight: 2, pieces.Pawn: 8}
    PIECE_STARTING_LOCATIONS = {pieces.King: (0, "E"), pieces.Queen: (0, "D"), pieces.Rook: (0, "A"),
                                pieces.Bishop: (0, "C"), pieces.Knight: (0, "B"), pieces.Pawn: (1, "A")}

    def __init__(self):
        self.board = self.generate_board()
        self.generate_board()
        self.initiate_pieces()
        self.active_player = pieces.Colours.WHITE.value

    def generate_board(self):
        return [{string.ascii_uppercase[index]: self.EMPTY_SPACE for index in range(self.BOARD_SIZE)} for _ in
                range(self.BOARD_SIZE)[::-1]]

    def __call__(self):
        """initiates the board, prints the board, contains game loop."""
        print(self)

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

    def fetch_board_square(self, coors):
        return self.board[coors[0]][coors[1]]

    def moves_in_direction(self, coordinates):
        max_moves_in_direction = self.BOARD_SIZE - 1
        moves_upwards = max_moves_in_direction - coordinates[0]
        moves_downwards = -(max_moves_in_direction - moves_upwards)
        moves_to_the_right = max_moves_in_direction - string.ascii_uppercase.index(coordinates[1])
        moves_to_the_left = -(max_moves_in_direction - moves_to_the_right)
        return {"left": moves_to_the_left, "right": moves_to_the_right, "down": moves_downwards, "up": moves_upwards}

    def possible_moves_for_board_position(self, coordinates):
        """For a piece on the board, get the rules for moving it,
        and return a subset of possible moves in context of the board position REGARDLESS of current board state."""
        move_rules = self.board[coordinates[0]][coordinates[1]].move_rules
        possible_moves_subset = []
        max_moves_in_directions = self.moves_in_direction(coordinates)
        for vector in move_rules:
            subset_vector = []
            for element in vector:
                if max_moves_in_directions["down"] <= element[0] <= max_moves_in_directions["up"] and \
                        max_moves_in_directions["left"] <= element[1] <= max_moves_in_directions["right"]:
                    subset_vector.append(element)
            possible_moves_subset.append(subset_vector)
        return possible_moves_subset

    def add_delta_to_coors(self, coordinates, delta):
        new_coors_y = coordinates[0] + delta[0]
        new_coors_x = self.modify_horizontal_coor(coordinates[1], delta[1])
        return new_coors_y, new_coors_x

    def collision_check_general(self, coordinates):
        possible_moves_subset = self.possible_moves_for_board_position(coordinates)
        legal_moves = []
        for vector in possible_moves_subset:
            for step in vector:
                square_to_check = self.add_delta_to_coors(coordinates, step)
                if self.board[square_to_check[0]][square_to_check[1]] == self.EMPTY_SPACE:
                    legal_moves.append(square_to_check)
                    continue
                if self.board[square_to_check[0]][square_to_check[1]].colour == \
                        self.board[coordinates[0]][coordinates[1]].colour:
                    break
                else:
                    legal_moves.append(square_to_check)
                    break
        return legal_moves

    def modify_horizontal_coor(self, coordinate, delta):
        return string.ascii_uppercase[string.ascii_uppercase.index(coordinate) + delta]

    def collision_check_pawn(self, coordinates):
        possible_moves = []
        y_delta = 1 if self.board[coordinates[0]][coordinates[1]].colour == pieces.Colours.WHITE.value else -1
        square_in_front = ((coordinates[0] + y_delta), coordinates[1])
        if self.board[square_in_front[0]][square_in_front[1]] == self.EMPTY_SPACE:  # space ahead is free
            possible_moves.append(square_in_front)
        left_diagonal = (
            (coordinates[0] + y_delta), self.modify_horizontal_coor(coordinates[1], -1))
        right_diagonal = (
            (coordinates[0] + y_delta), self.modify_horizontal_coor(coordinates[1], +1))
        if coordinates[1] != "A" and self.board[left_diagonal[0]][left_diagonal[1]] != self.EMPTY_SPACE and \
                self.board[left_diagonal[0]][left_diagonal[1]].colour != \
                self.board[coordinates[0]][coordinates[1]].colour:
            possible_moves.append(left_diagonal)
        if coordinates[1] != "H" and self.board[right_diagonal[0]][right_diagonal[1]] != self.EMPTY_SPACE and \
                self.board[right_diagonal[0]][right_diagonal[1]].colour != \
                self.board[coordinates[0]][coordinates[1]].colour:
            possible_moves.append(right_diagonal)
        starting_row = 1 if self.board[coordinates[0]][coordinates[1]].colour == pieces.Colours.WHITE.value else 6
        double_move = ((coordinates[0] + (2 * y_delta)), coordinates[1])
        # double_move = self.board[coordinates[0] + (2 * y_delta)][coordinates[1]]
        if coordinates[0] == starting_row and self.board[square_in_front[0]][square_in_front[1]] == self.EMPTY_SPACE and \
                self.board[double_move[0]][double_move[1]] == self.EMPTY_SPACE:
            possible_moves.append(double_move)
        return possible_moves

    def collision_check(self, coordinates):
        if isinstance(self.board[coordinates[0]][coordinates[1]], pieces.Pawn):
            return self.collision_check_pawn(coordinates)
        else:
            return self.collision_check_general(coordinates)

    def select_coordinates(self, string_prompt):
        input_is_correct = False
        while not input_is_correct:
            player_input = input(string_prompt)
            if len(player_input) == 2:
                if player_input[0].upper() in string.ascii_uppercase[0:8]:
                    if player_input[1].isdigit() and 1 <= int(player_input[1]) <= 8:
                        input_is_correct = True
        coordinates_tuple = ((int(player_input[1]) - 1), player_input[0].upper())
        return coordinates_tuple

    def move_piece(self, starting_coordinates, destination_coordinates):
        if destination_coordinates is not False:
            self.board[destination_coordinates[0]][destination_coordinates[1]] = self.board[starting_coordinates[0]][
                starting_coordinates[1]]
            self.board[starting_coordinates[0]][starting_coordinates[1]] = self.EMPTY_SPACE
            if isinstance(self.fetch_board_square(starting_coordinates), pieces.King) and \
                    destination_coordinates in pieces.King.left_right_castles:

        else:
            return None

    def square_not_empty_check(self, coors):
        return True if self.board[coors[0]][coors[1]] != self.EMPTY_SPACE else False

    def piece_matches_player_check(self, coors):
        return True if self.board[coors[0]][coors[1]].colour == self.active_player else False

    def get_valid_piece_coors(self):
        while True:
            origin_coors = self.select_coordinates(f'Type in the coordinates of a {self.active_player} piece!')
            if self.square_not_empty_check(origin_coors) and self.piece_matches_player_check(origin_coors):
                break
        return origin_coors

    def get_valid_target_or_cancel_move(self, origin_coors):
        legal_moves = self.collision_check(origin_coors)
        print(legal_moves)
        move_is_valid = False
        while not move_is_valid:
            target_coordinates = self.select_coordinates("Type in the coordinates of where you want to move the piece!")
            if target_coordinates in legal_moves:
                move_is_valid = True
            elif target_coordinates == origin_coors:
                return False
        return target_coordinates

    def change_player(self):
        if self.active_player == pieces.Colours.WHITE.value:
            self.active_player = pieces.Colours.BLACK.value
        else:
            self.active_player = pieces.Colours.WHITE.value

    def turn_sequence(self):
        while True:
            print(self)
            origin_coors = self.get_valid_piece_coors()
            destination_coors = self.get_valid_target_or_cancel_move(origin_coors)
            self.move_piece(origin_coors, destination_coors)
            self.change_player()


if __name__ == "__main__":
    board_instance = ChessBoard()
    board_instance.turn_sequence()
