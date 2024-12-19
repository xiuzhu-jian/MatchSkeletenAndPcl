import json
import os
from datetime import datetime

import numpy as np


def get_timestamp_ms_in_skeleton_filename(filename: str):
    if not (filename.startswith('skeleton_data_') and filename.endswith('.json')):
        print(f'error filename: {filename}')
        return -1
    return float(filename.rsplit('_', 1)[-1].rsplit('.', 1)[0])


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


def _sort_key(element):
    return element[1]


def get_files_list(folder_path: str, get_timestamp_ms_func):
    files_list = os.listdir(folder_path)
    file_and_timestamp_ms_list = []
    for file_name in files_list:
        file_and_timestamp_ms_list.append((file_name, get_timestamp_ms_func(file_name)))
    file_and_timestamp_ms_list = sorted(file_and_timestamp_ms_list, key=_sort_key, reverse=False)
    return file_and_timestamp_ms_list


def read_pcl_from_txt(file_path):
    try:
        data = np.loadtxt(file_path)
    except ValueError as e:
        print(f'{file_path}: {e}')
        return None

    if data.ndim == 1:
        if len(data) == 0:
            return None
        else:
            return [{"x": data[0], "y": data[1], "z": data[2]}]
    else:
        return [{"x": row[0], "y": row[1], "z": row[2]} for row in data]


def convert_skeleton_json_to_matrix(skeleton_json):
    matrix = []
    for keypoint in skeleton_json:
        matrix.append([keypoint['x'], keypoint['y'], keypoint['z']])
    return np.array(matrix)


def compute_bbox(nodes):
    nodes = np.array(nodes)
    min_vals = np.min(nodes, axis=0)
    max_vals = np.max(nodes, axis=0)
    return min_vals, max_vals


def compute_dimensions(min_vals, max_vals):
    center = (min_vals + max_vals) / 2.0
    dimensions = max_vals - min_vals
    return center, dimensions


def get_bbox(skeleton_points):
    min_vals, max_vals = compute_bbox(skeleton_points)
    center, dimensions = compute_dimensions(min_vals, max_vals)
    gt_bbox = {
        "center": center.tolist(),
        "dimensions": dimensions.tolist()
    }
    center = gt_bbox["center"]
    dimensions = gt_bbox["dimensions"]
    bbox_data = {
        "x": center[0],
        "y": center[1],
        "z": center[2],
        "w": dimensions[0],
        "l": dimensions[1] + 0.2,
        "h": dimensions[2]
    }
    return bbox_data


def make_output_dir(addition_str: str = ''):
    path = f'output/point_cloud_info_generated_at_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'
    if addition_str != '':
        path += f'_{addition_str}'
    os.makedirs(path, exist_ok=True)
    return path


def is_in_arena(x, y, z, x_min, x_max, y_min, y_max, z_min, z_max):
    if not x_min < x < x_max:
        print(f'error: x out of arena, x:{x}, x_min:{x_min}, x_max:{x_max}')
        return False
    if not y_min < y < y_max:
        print(f'error: y out of arena, y:{y}, y_min:{y_min}, y_max:{y_max}')
        return False
    if not z_min < z < z_max:
        print(f'error: z out of arena, z:{z}, z_min:{z_min}, z_max:{z_max}')
        return False
    return True


def get_posture_and_action_label(pcl_filename: str):
    return pcl_filename.split('_', 2)[:2]
