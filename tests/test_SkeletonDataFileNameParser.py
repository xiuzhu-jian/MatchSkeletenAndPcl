from NameParser.SkeletonDataFileNameParser import get_timestamp_ms_in_skeleton_filename


def test_get_timestamp_ms_in_skeleton_filename():
    assert get_timestamp_ms_in_skeleton_filename('skeleton_data_1720507907557.7573.json') == 1720507907557.7573
    assert get_timestamp_ms_in_skeleton_filename('skeleton_data_1720507907557.7573.jso') == -1
    assert get_timestamp_ms_in_skeleton_filename('keleton_data_1720507907557.7573.json') == -1
