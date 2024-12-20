import pytest
from CoordConvertion.L515Coord import *


@pytest.mark.parametrize('pos_idx, row_idx', [
    (0, 0),
    (1, 0),
    (2, 0),
    (3, 0),
    (4, 1),
    (5, 1),
    (6, 1),
    (7, 1),
    (8, 2),
    (9, 2),
    (10, 2),
    (11, 2),
    (12, 3),
    (13, 3),
    (14, 3),
    (15, 3),
])
def test_pos_idx_to_row_idx(pos_idx, row_idx):
    assert pos_idx_to_row_idx(pos_idx) == row_idx


@pytest.mark.parametrize('pos_idx, coord', [
    (0, [1.5, -3.2, 0.92]),
    (1, [0, -3.2, 0.92]),
    (2, [0, -3.2, 0.92]),
    (3, [-1.5, -3.2, 0.92]),
    (4, [-1.5, -3.2, 0.92]),
    (5, [0, -3.2, 0.92]),
    (6, [0, -3.2, 0.92]),
    (7, [1.5, -3.2, 0.92]),
    (8, [0, -3.2, 0.92]),
    (9, [0, -3.2, 0.92]),
    (10, [0, -3.2, 0.92]),
    (11, [0, -3.2, 0.92]),
    (12, [0, -2.6, 0.92]),
    (13, [0, -2.6, 0.92]),
    (14, [0, -2.6, 0.92]),
    (15, [0, -2.6, 0.92]),
])
def test_sit_pos_idx_to_l515_coord(pos_idx, coord):
    assert sit_pos_idx_to_l515_coord(pos_idx) == coord
