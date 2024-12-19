def parse_vc_folder_name(vc_folder_name: str):
    sensor_mounting, _, _, vc_id = vc_folder_name.split('-')
    return sensor_mounting, int(vc_id)
