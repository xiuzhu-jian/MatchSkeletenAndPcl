def parse_arena(point_cloud_data_filename: str):
    return list(map(float, point_cloud_data_filename.split('_')[2:8]))

def parse_height(point_cloud_data_filename: str):
    return float(point_cloud_data_filename.split('_')[8])


def get_timestamp_ms_in_pcl_filename(filename: str):
    sec, rest = filename.rsplit('_', 1)[-1].rsplit('.', 1)[0].split('.')
    rest_len = len(rest)
    if rest_len < 3:
        msec = rest + '0' * (3 - rest_len)
        tail = ''
    else:
        msec = rest[:3]
        tail = rest[3:]
    return float(sec + msec + '.' + tail)
