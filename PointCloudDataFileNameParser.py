def parse_arena(point_cloud_data_filename: str):
    return list(map(float, point_cloud_data_filename.split('_')[2:8]))

def parse_height(point_cloud_data_filename: str):
    return float(point_cloud_data_filename.split('_')[8])