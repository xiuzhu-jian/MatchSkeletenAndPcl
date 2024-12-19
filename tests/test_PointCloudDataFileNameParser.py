from PointCloudDataFileNameParser import *


def test_get_arena():
    assert get_arena('stand_stand_-2.00_2.00_-2.00_2.00_0.00_2.00_2.45_2.00_1733984702.6237457.txt') == [
        -2.0, 2.0, -2.0, 2.0, 0.0, 2.0
    ]


def test_get_height():
    assert get_height('stand_stand_-2.00_2.00_-2.00_2.00_0.00_2.00_2.45_2.00_1733984702.6237457.txt') == 2.45
