from FilenameParser import *


def test_parse_filename():
    assert parse_filename('stand-40-s_0_20241212-1425') == ('stand', 0, '20241212-1425')
