import os
from datetime import datetime

from Tools.CollectionNameCreater import create_collection_name


def create_output_folder():
    path = f'output/point_cloud_info_generated_at_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'
    os.makedirs(path, exist_ok=True)
    return path


def create_child_folder(parent_folder_fullpath, child_folder_name):
    folder_path = os.path.join(parent_folder_fullpath, child_folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def create_match_output_folder(output_folder, posture, pos_idx, collection_id, vc_id, sensor_mounting):
    generated_data_folder_name = create_collection_name(posture, pos_idx, collection_id, vc_id, sensor_mounting)
    return create_child_folder(output_folder, generated_data_folder_name)


def create_data_output_folder(output_folder):
    return create_child_folder(output_folder, 'Data')


def create_match_log_output_folder(output_folder):
    return create_child_folder(output_folder, 'MatchLog')


def create_coord_convertion_log_output_folder(output_folder):
    return create_child_folder(output_folder, 'CoordConvertionLog')
