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
        self.active_player = pieces.colors.WHITE.value

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
        for color in pieces.colors:
            for piece, number_of_same_pieces in self.REPEATS.items():
                if color == pieces.colors.WHITE:
                    row_index = self.PIECE_STARTING_LOCATIONS[piece][0]
                else:
                    row_index = self.BOARD_SIZE - self.PIECE_STARTING_LOCATIONS[piece][0] - 1
                col_index = string.ascii_uppercase.index(self.PIECE_STARTING_LOCATIONS[piece][1])
                for index in range(number_of_same_pieces):
                    if index < 2:
                        col_index += - (col_index * index) + ((self.BOARD_SIZE - col_index - 1) * index)
                    else:
                        col_index -= 1
                    self.board[row_index][string.ascii_uppercase[col_index]] = piece(color.value)

    def modify_horizontal_coor(self, coordinate, delta):
        return string.ascii_uppercase[string.ascii_uppercase.index(coordinate) + delta]

    def moves_in_direction(self, coordinates):
        max_moves_in_direction = self.BOARD_SIZE - 1
        moves_upwards = max_moves_in_direction - coordinates[0]
        moves_downwards = -(max_moves_in_direction - moves_upwards)
        moves_to_the_right = max_moves_in_direction - string.ascii_uppercase.index(coordinates[1])
        moves_to_the_left = -(max_moves_in_direction - moves_to_the_right)
        return {"left": moves_to_the_left, "right": moves_to_the_right, "down": moves_downwards, "up": moves_upwards}

    def filter_positional_move_set(self, coordinates):
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

    def left_castle_collision_check(self, coors):
        if isinstance(self.board[coors[0]]['A'], pieces.Rook) and \
                self.board[coors[0]]['A'].color == self.fetch_board_square(coors).color:
            if self.board[coors[0]]['B'] == self.board[coors[0]]['C'] == self.board[coors[0]]['D'] == self.EMPTY_SPACE:
                return True

    def right_castle_collision_check(self, coors):
        if isinstance(self.board[coors[0]]['H'], pieces.Rook) and \
                self.board[coors[0]]['H'].color == self.fetch_board_square(coors).color:
            if self.board[coors[0]]['F'] == self.board[coors[0]]['G'] == self.EMPTY_SPACE:
                return True

    def castle_check_king(self, coors, move_set):
        """Removes the castling options from the relative move set if conditions are not met"""
        if not self.left_castle_collision_check(coors=coors):
            move_set[3] = [[0, -1]]
        if not self.right_castle_collision_check(coors=coors):
            move_set[5] = [[0, 1]]

    def collision_check_general_case(self, coordinates):
        possible_moves_subset = self.filter_positional_move_set(coordinates)
        legal_moves = []
        for vector in possible_moves_subset:
            for step in vector:
                square_to_check = self.add_delta_to_coors(coordinates, step)
                if self.board[square_to_check[0]][square_to_check[1]] == self.EMPTY_SPACE:
                    legal_moves.append(square_to_check)
                    continue
                if self.board[square_to_check[0]][square_to_check[1]].color == \
                        self.board[coordinates[0]][coordinates[1]].color:
                    break
                else:
                    legal_moves.append(square_to_check)
                    break
        return legal_moves

    def collision_check_king(self, coors):
        """If the king has not moved, performs check whether castling is possible, calls the collision check function
            and returns the move set"""
        move_set = self.fetch_board_square(coors).move_rules
        if not self.fetch_board_square(coors).moved:
            self.castle_check_king(coors, move_set)
        return self.collision_check_general_case(coors)

    def collision_check_pawn(self, coordinates):
        possible_moves = []
        y_delta = 1 if self.board[coordinates[0]][coordinates[1]].color == pieces.colors.WHITE.value else -1
        square_in_front = ((coordinates[0] + y_delta), coordinates[1])
        if self.board[square_in_front[0]][square_in_front[1]] == self.EMPTY_SPACE:  # space ahead is free
            possible_moves.append(square_in_front)
        left_diagonal = (
            (coordinates[0] + y_delta), self.modify_horizontal_coor(coordinates[1], -1))
        right_diagonal = (
            (coordinates[0] + y_delta), self.modify_horizontal_coor(coordinates[1], +1))
        if coordinates[1] != "A" and self.board[left_diagonal[0]][left_diagonal[1]] != self.EMPTY_SPACE and \
                self.board[left_diagonal[0]][left_diagonal[1]].color != \
                self.board[coordinates[0]][coordinates[1]].color:
            possible_moves.append(left_diagonal)
        if coordinates[1] != "H" and self.board[right_diagonal[0]][right_diagonal[1]] != self.EMPTY_SPACE and \
                self.board[right_diagonal[0]][right_diagonal[1]].color != \
                self.board[coordinates[0]][coordinates[1]].color:
            possible_moves.append(right_diagonal)
        starting_row = 1 if self.board[coordinates[0]][coordinates[1]].color == pieces.colors.WHITE.value else 6
        double_move = ((coordinates[0] + (2 * y_delta)), coordinates[1])
        # double_move = self.board[coordinates[0] + (2 * y_delta)][coordinates[1]]
        if coordinates[0] == starting_row and self.board[square_in_front[0]][square_in_front[1]] == self.EMPTY_SPACE \
                and self.board[double_move[0]][double_move[1]] == self.EMPTY_SPACE:
            possible_moves.append(double_move)
        return possible_moves

    def collision_check_all_cases(self, coordinates):
        if isinstance(self.fetch_board_square(coordinates), pieces.Pawn):
            return self.collision_check_pawn(coordinates)
        elif isinstance(self.fetch_board_square(coordinates), pieces.King):
            return self.collision_check_king(coordinates)
        else:
            return self.collision_check_general_case(coordinates)

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

    def move_and_transform_pawn(self, starting_coors, destination_coors):
        self.board[destination_coors[0]][destination_coors[1]] = \
            self.fetch_board_square(starting_coors).choose_pawn_transformation()
        self.board[starting_coors[0]][starting_coors[1]] = self.EMPTY_SPACE

    def check_what_move_to_perform(self, starting_coors, destination_coors):
        if isinstance(self.fetch_board_square(starting_coors), pieces.King) and starting_coors[1] == 'E' and \
                starting_coors[0] in (0, 7) and destination_coors[1] in ('C', 'G') and \
                self.fetch_board_square(starting_coors).moved is False:
            self.make_castle(starting_coors, destination_coors)
            return None
        if isinstance(self.fetch_board_square(starting_coors), pieces.Pawn) and destination_coors[0] in (0, 7):
            self.move_and_transform_pawn(starting_coors, destination_coors)
            return None
        else:
            self.move_piece(starting_coors, destination_coors)
    #
    # def check_if_square_is_threatened(self, coordinates, color):
    #     for vector in

    def make_castle(self, starting_coors, destination_coors):
        if destination_coors[1] == 'C':
            rook_start_coors = [starting_coors[0], 'A']
            rook_destination_coors = [starting_coors[0], 'D']
            self.move_piece(starting_coors, destination_coors)
            self.move_piece(rook_start_coors, rook_destination_coors)
        elif destination_coors[1] == 'G':
            rook_start_coors = [starting_coors[0], 'H']
            rook_destination_coors = [starting_coors[0], 'F']
            self.move_piece(starting_coors, destination_coors)
            self.move_piece(rook_start_coors, rook_destination_coors)

    def move_piece(self, starting_coors, destination_coors):
        if destination_coors is not False:
            self.board[destination_coors[0]][destination_coors[1]] = self.fetch_board_square(starting_coors)
            self.board[starting_coors[0]][starting_coors[1]] = self.EMPTY_SPACE
        else:
            return None

    def square_not_empty_check(self, coors):
        return True if self.board[coors[0]][coors[1]] != self.EMPTY_SPACE else False

    def piece_matches_player_check(self, coors):
        return True if self.board[coors[0]][coors[1]].color == self.active_player else False

    def get_valid_piece_coors(self):
        while True:
            origin_coors = self.select_coordinates(f'Type in the coordinates of a {self.active_player} piece!')
            if self.square_not_empty_check(origin_coors) and self.piece_matches_player_check(origin_coors):
                break
        return origin_coors

    def get_valid_target_or_cancel_move(self, origin_coors):
        legal_moves = self.collision_check_all_cases(origin_coors)
        move_is_valid = False
        while not move_is_valid:
            target_coordinates = self.select_coordinates("Type in the coordinates of where you want to move the piece!")
            if target_coordinates in legal_moves:
                move_is_valid = True
            elif target_coordinates == origin_coors:
                return False
        return target_coordinates

    def change_player(self):
        if self.active_player == pieces.colors.WHITE.value:
            self.active_player = pieces.colors.BLACK.value
        else:
            self.active_player = pieces.colors.WHITE.value

    def fetch_board_square(self, coors):
        return self.board[coors[0]][coors[1]]

    # def check_king_castle_conditions(self, move_set, coors):
    #     if self.fetch_board_square(coors).moved is False:
    #         possible_castles = [False, False]
    #         rook_starting_positions = [(coors[0], 'A'), (coors[0], 'H')]
    #         squares_between_king_and_rook = [[(coors[0], 'C'), (coors[0], 'D')],
    #                                          [(coors[0], 'F'), (coors[0], 'G')]]
    #         for idx in range(len(rook_starting_positions)):
    #             if isinstance(self.fetch_board_square(rook_starting_positions[idx]), pieces.Rook):
    #                 if self.fetch_board_square(rook_starting_positions[idx]).moved is False:
    #                     if all(squares_between_king_and_rook[idx]) == self.EMPTY_SPACE:
    #                         possible_castles[idx] = True
    #         for index in range(len(possible_castles)):
    #             if possible_castles[index] is False:
    #                 move_set.pop(move_set.index(pieces.King.left_right_castles[index]))
    #         return move_set
    #     return move_set

    def turn_sequence(self):
        while True:
            print(self)
            origin_coors = self.get_valid_piece_coors()
            destination_coors = self.get_valid_target_or_cancel_move(origin_coors)
            self.check_what_move_to_perform(origin_coors, destination_coors)
            self.change_player()


if __name__ == "__main__":
    board_instance = ChessBoard()
    board_instance.board[0]['F'] = board_instance.EMPTY_SPACE
    board_instance.board[0]['G'] = board_instance.EMPTY_SPACE
    board_instance.board[6]['E'] = pieces.Pawn()
    board_instance.turn_sequence()
