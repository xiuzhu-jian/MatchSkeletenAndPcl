from VCFolderNameParser import parse_vc_folder_name


def test_parse_vc_folder_name():
    assert parse_vc_folder_name('Ceiling-vc1-ip-50000') == ('Ceiling', 50000)
