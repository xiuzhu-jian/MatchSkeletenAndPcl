from CoordinatesConverter import d455_to_vayyar_care
import pytest


@pytest.mark.parametrize('x, y, z, d455_x, d455_y, d455_z, expected', [
    (2, 2, 2, -3, 1, 3, (5, 3, 1)),
    (-2, -2, 2, -3, 1, 3, (1, 3, 5)),
])
def test_d455_to_vayyar_care(x, y, z, d455_x, d455_y, d455_z, expected):
    assert expected == d455_to_vayyar_care(x, y, z, d455_x, d455_y, d455_z)
