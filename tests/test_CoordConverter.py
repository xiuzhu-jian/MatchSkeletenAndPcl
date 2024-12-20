import pytest
from CoordConvertion.CoordConverter import *

DIFF = 1e-6


@pytest.mark.parametrize('l515_point_coord, l515_world_coord, result', [
    ((1.5, -0.8, 2), (0, -3.2, 0.9), (1.5, -1.2, 1.7)),  # stand row 2, sit row 0, 1, 2
    ((0, -0.8, 2), (1.5, -3.2, 0.9), (1.5, -1.2, 1.7)),  # sit pos 0, 7
    ((0, -0.8, 2), (-1.5, -3.2, 0.9), (-1.5, -1.2, 1.7)),  # sit pos 3, 4
    ((1.5, -0.8, 2), (0, -2.6, 0.9), (1.5, -0.6, 1.7)),  # stand row 3, sit row 3
])
def test_point_from_front_l515_to_world(l515_point_coord, l515_world_coord, result):
    new_coord = point_from_front_l515_to_world(l515_point_coord, l515_world_coord)
    assert abs(new_coord[0] - result[0]) < DIFF
    assert abs(new_coord[1] - result[1]) < DIFF
    assert abs(new_coord[2] - result[2]) < DIFF


@pytest.mark.parametrize('l515_point_coord, l515_world_coord, result', [
    ((1.5, -0.8, 2), (0, 2.46, 0.9), (-1.5, 0.46, 1.7)),  # stand row 0
    ((1.5, -0.8, 2), (0, 3.64, 0.9), (-1.5, 1.64, 1.7)),  # stand row 1
])
def test_point_from_back_l515_to_world(l515_point_coord, l515_world_coord, result):
    new_coord = point_from_back_l515_to_world(l515_point_coord, l515_world_coord)
    assert abs(new_coord[0] - result[0]) < DIFF
    assert abs(new_coord[1] - result[1]) < DIFF
    assert abs(new_coord[2] - result[2]) < DIFF


@pytest.mark.parametrize('world_coord, vc_world_coord, result', [
    ((1.5, -1.2, 1.78), (0.1, -0.1, 2.45), (1.4, -1.1, 1.78)),
    ((1.5, -1.2, 1.78), (-0.1, 0.1, 2.45), (1.6, -1.3, 1.78)),
    ((1.5, -1.2, 1.78), (-0.15, -2, 1.53), (1.65, 0.8, 1.78)),
    ((1.5, -1.2, 1.78), (0.15, -2, 1.53), (1.35, 0.8, 1.78)),
])
def test_point_from_world_to_vc(world_coord, vc_world_coord, result):
    new_coord = point_from_world_to_vc(world_coord, vc_world_coord)
    assert abs(new_coord[0] - result[0]) < DIFF
    assert abs(new_coord[1] - result[1]) < DIFF
    assert abs(new_coord[2] - result[2]) < DIFF
