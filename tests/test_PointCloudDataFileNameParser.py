from NameParser.PclDataFileNameParser import *


def test_parse_arena():
    assert parse_arena('stand_stand_-2.00_2.00_-2.00_2.00_0.00_2.00_2.45_2.00_1733984702.6237457.txt') == [
        -2.0, 2.0, -2.0, 2.0, 0.0, 2.0
    ]


def test_parse_height():
    assert parse_height('stand_stand_-2.00_2.00_-2.00_2.00_0.00_2.00_2.45_2.00_1733984702.6237457.txt') == 2.45


def test_get_timestamp_ms_in_pcl_filename():
    assert get_timestamp_ms_in_pcl_filename(
        'Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507915.876667.txt') == 1720507915876.667
    assert get_timestamp_ms_in_pcl_filename(
        'Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507916.8781.txt') == 1720507916878.1
    assert get_timestamp_ms_in_pcl_filename(
        'Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507916.8.txt') == 1720507916800
