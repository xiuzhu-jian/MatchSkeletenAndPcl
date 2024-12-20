stand_row_idx_to_L515_coord = {
    0: (0, 2.46, 0.92),
    1: (0, 3.64, 0.92),
    2: (0, -3.2, 0.92),
    3: (0, -2.6, 0.92)
}

sit_row_idx_to_L515_coord = {
    0: (0, -3.2, 0.92),
    1: (0, -3.2, 0.92),
    2: (0, -3.2, 0.92),
    3: (0, -2.6, 0.92)
}


def pos_idx_to_row_idx(pos_idx):
    return pos_idx // 4


def stand_pos_idx_to_l515_coord(pos_idx):
    return stand_row_idx_to_L515_coord[pos_idx_to_row_idx(pos_idx)]


def sit_pos_idx_to_l515_coord(pos_idx):
    coord = list(sit_row_idx_to_L515_coord[pos_idx_to_row_idx(pos_idx)])
    special_pos_to_x_coord = {
        0: 1.5,
        7: 1.5,
        3: -1.5,
        4: -1.5
    }
    if pos_idx in special_pos_to_x_coord:
        coord[0] = special_pos_to_x_coord[pos_idx]
    return coord
