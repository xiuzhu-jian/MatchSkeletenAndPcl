import numpy as np

from Tool import *


def test_get_timestamp_ms_in_skeleton_filename():
    assert get_timestamp_ms_in_skeleton_filename('skeleton_data_1720507907557.7573.json') == 1720507907557.7573
    assert get_timestamp_ms_in_skeleton_filename('skeleton_data_1720507907557.7573.jso') == -1
    assert get_timestamp_ms_in_skeleton_filename('keleton_data_1720507907557.7573.json') == -1


def test_get_timestamp_ms_in_pcl_filename():
    assert get_timestamp_ms_in_pcl_filename(
        'Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507915.876667.txt') == 1720507915876.667
    assert get_timestamp_ms_in_pcl_filename(
        'Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507916.8781.txt') == 1720507916878.1
    assert get_timestamp_ms_in_pcl_filename(
        'Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507916.8.txt') == 1720507916800


def test_get_skeleton_files_list():
    files_list = [
        (r"skeleton_data_1720507907557.7573.json", 1720507907557.7573),
        (r"skeleton_data_1720507907591.0806.json", 1720507907591.0806),
        (r"skeleton_data_1720507907624.4028.json", 1720507907624.4028),
        (r"skeleton_data_1720507907657.7258.json", 1720507907657.7258),
        (r"skeleton_data_1720507907691.0476.json", 1720507907691.0476),
        (r"skeleton_data_1720507907724.3704.json", 1720507907724.3704),
        (r"skeleton_data_1720507907757.6917.json", 1720507907757.6917),
        (r"skeleton_data_1720507907791.014.json", 1720507907791.014),
        (r"skeleton_data_1720507907824.335.json", 1720507907824.335),
        (r"skeleton_data_1720507907857.6567.json", 1720507907857.6567),
        (r"skeleton_data_1720507907890.9773.json", 1720507907890.9773),
        (r"skeleton_data_1720507907924.2988.json", 1720507907924.2988),
        (r"skeleton_data_1720507907957.6191.json", 1720507907957.6191),
        (r"skeleton_data_1720507907990.9402.json", 1720507907990.9402),
        (r"skeleton_data_1720507908024.26.json", 1720507908024.26),
        (r"skeleton_data_1720507908057.581.json", 1720507908057.581),
        (r"skeleton_data_1720507908090.9082.json", 1720507908090.9082),
        (r"skeleton_data_1720507908124.236.json", 1720507908124.236),
        (r"skeleton_data_1720507908157.5627.json", 1720507908157.5627),
        (r"skeleton_data_1720507908190.8901.json", 1720507908190.8901),
        (r"skeleton_data_1720507908224.2166.json", 1720507908224.2166),
        (r"skeleton_data_1720507908257.5435.json", 1720507908257.5435),
        (r"skeleton_data_1720507908290.8694.json", 1720507908290.8694),
        (r"skeleton_data_1720507908324.196.json", 1720507908324.196),
    ]
    assert get_files_list('TestData/skeleton', get_timestamp_ms_in_skeleton_filename) == files_list


def test_get_pcl_files_list():
    files_list = [
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507915.7595334.txt", 1720507915759.5334),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507915.876667.txt", 1720507915876.667),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507915.998087.txt", 1720507915998.087),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507916.1189432.txt", 1720507916118.9432),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507916.2781782.txt", 1720507916278.1782),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507916.3982537.txt", 1720507916398.2537),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507916.517765.txt", 1720507916517.765),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507916.6380396.txt", 1720507916638.0396),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507916.7582705.txt", 1720507916758.2705),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507916.8781.txt", 1720507916878.1),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507916.997608.txt", 1720507916997.608),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507917.1193173.txt", 1720507917119.3173),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507917.2370727.txt", 1720507917237.0727),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507917.3580878.txt", 1720507917358.0878),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507917.4787402.txt", 1720507917478.7402),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507917.5976331.txt", 1720507917597.6331),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507917.7182732.txt", 1720507917718.2732),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507917.858428.txt", 1720507917858.428),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507917.9782112.txt", 1720507917978.2112),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507918.0989342.txt", 1720507918098.9342),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507918.2194026.txt", 1720507918219.4026),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507918.3386285.txt", 1720507918338.6285),
        ("Wash feet_Wash feet_-1.50_1.50_0.20_2.80_0.00_1.80_1.60_2.80_1720507918.4776878.txt", 1720507918477.6878),
    ]
    assert get_files_list('TestData/pcl', get_timestamp_ms_in_pcl_filename) == files_list


def test_convert_skeleton_to_matrix():
    test_data = {
        "skeleton": [
            {
                "index": 0,
                "x": 1,
                "y": 1,
                "z": 1
            },
            {
                "index": 1,
                "x": 2,
                "y": 2,
                "z": 2
            },
            {
                "index": 2,
                "x": 3,
                "y": 3,
                "z": 3
            },
        ]
    }
    assert np.array_equal(convert_skeleton_json_to_matrix(test_data['skeleton']), np.array([
        [1, 1, 1],
        [2, 2, 2],
        [3, 3, 3],
    ]))
