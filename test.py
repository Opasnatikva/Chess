BOARD_SIZE = 8


def move_rules_rook():
    coor_deltas = []
    for change in range(-BOARD_SIZE + 1, BOARD_SIZE):
        new_position_horizontal = (0, change)
        new_position_vertical = (change, 0)
        if new_position_horizontal != (0, 0) and coor_deltas.count(new_position_horizontal) == 0:
            coor_deltas.append(new_position_horizontal)
        if new_position_vertical != (0, 0) and coor_deltas.count(new_position_vertical) == 0:
            coor_deltas.append(new_position_vertical)
    return coor_deltas


def new_move_rules_bishop():
    coor_deltas = [[], [], [], []]
    for delta in range(1, BOARD_SIZE):
        delta_right_up = [delta, delta]
        delta_right_down = [delta, -delta]
        delta_left_up = [-delta, delta]
        delta_left_down = [-delta, -delta]
        coor_deltas[0].append(delta_right_up)
        coor_deltas[1].append(delta_right_down)
        coor_deltas[2].append(delta_left_up)
        coor_deltas[3].append(delta_left_down)
    return coor_deltas


print(move_rules_rook())
a = new_move_rules_bishop()
for element in a:
    print(element)
