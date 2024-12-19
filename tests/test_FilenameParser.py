from PclDataFolderNameParser import *


def test_parse_filename():
    assert parse_pcl_data_folder_name('stand-40-s_0_20241212-1425') == ('stand', 0, '20241212-1425')
