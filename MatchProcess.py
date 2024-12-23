import json

from CoordConvertion.CoordConverter import point_from_front_l515_to_world, point_from_back_l515_to_world, \
    point_from_world_to_vc
from NameParser.PclDataFileNameParser import get_timestamp_ms_in_pcl_filename
from NameParser.SkeletonDataFileNameParser import get_timestamp_ms_in_skeleton_filename
from Reporters.CoordConvertionReporter import CoordConverterReporter
from CoordConvertion.L515Coord import pos_idx_to_row_idx
from Definitions.SkeletonDef import KEYPOINT_INDEX_TO_NAME
from Reporters.MatchResultReporter import MatchResultReporter
from Tools.CollectionNameCreater import create_collection_name
from Tools.Tool import *
from CoordConvertion.VCCoord import VC_ID_TO_COORD

X_CORRECTION_IN_METERS = 0.25
LABEL_TIMESTAMP_CORRECTION_IN_MILLISECONDS = 0


def match(skeleton_data_folder: str, pcl_data_folder: str,
          data_output_dir,
          match_log_output_folder: str,
          coord_convertion_log_output_folder: str,
          id_str, label_str, config, pos_idx, vc_id,
          sensor_mounting):
    skeleton_files = get_files_list_sorted_by_time(skeleton_data_folder, get_timestamp_ms_in_skeleton_filename)
    pcl_files = get_files_list_sorted_by_time(pcl_data_folder, get_timestamp_ms_in_pcl_filename)

    reporter = MatchResultReporter()
    reporter.on_start(match_log_output_folder,
                      create_collection_name(label_str, pos_idx, id_str, vc_id, sensor_mounting))

    matched_data_list = []

    skeleton_file_pointer = 0
    skeleton_files_len = len(skeleton_files)
    for pcl_file_index, (pcl_filename, pcl_timestamp) in enumerate(pcl_files):
        while True:
            sk_filename, sk_timestamp = skeleton_files[skeleton_file_pointer]
            if sk_timestamp + LABEL_TIMESTAMP_CORRECTION_IN_MILLISECONDS < pcl_timestamp:
                skeleton_file_pointer += 1
                if skeleton_file_pointer == skeleton_files_len:
                    break
            else:
                break

        if skeleton_file_pointer == skeleton_files_len:
            print(f'skeleton enumeration end, pcl_file_index={pcl_file_index}')
            break

        reporter.report(pcl_filename, sk_filename, float(pcl_timestamp), float(sk_timestamp))
        matched_data_list.append(
            [os.path.join(pcl_data_folder, pcl_filename),
             os.path.join(skeleton_data_folder, sk_filename),
             str(pcl_timestamp),
             str(sk_timestamp)])

    reporter.on_finish()

    process(matched_data_list, config, data_output_dir, id_str, label_str, pos_idx, vc_id, sensor_mounting,
            coord_convertion_log_output_folder)


def generate_target_info(skeleton_json, posture, action, config, pos_idx, vc_id):
    skeleton_in_vc_coord_system, skeleton_mat, msg = covert_skeleton_to_vc_coordinate_system(skeleton_json, config,
                                                                                             pos_idx,
                                                                                             vc_id, posture)
    if skeleton_in_vc_coord_system is None:
        return None, msg
    target_info = {
        'posture': posture,
        'action': action,
        'isfall': 'no',
        'skeleton': skeleton_in_vc_coord_system,
        'bbox': get_bbox(skeleton_mat)
    }
    return target_info, msg


def generate_targets_info(targets_json, posture, action, config, pos_idx, vc_id):
    targets_info = []
    for target in targets_json:
        target_info, msg = generate_target_info(target['skeleton'], posture, action, config, pos_idx, vc_id)
        if target_info is None:
            return None, msg
        targets_info.append(target_info)
    return targets_info, 'no target in targets_json'


def covert_skeleton_to_vc_coordinate_system(skeleton_json, config, pos_idx, vc_id, posture):
    if posture == 'stand' and pos_idx_to_row_idx(pos_idx) in (0, 1):
        converter = point_from_back_l515_to_world
    else:
        converter = point_from_front_l515_to_world
    vc_world_coord = VC_ID_TO_COORD[vc_id]

    skeleton_data_in_pcl_coordinate_system = []
    skeleton_array = []
    for keypoint in skeleton_json:
        xv, yv, zv = converter((keypoint['x'], keypoint['y'], keypoint['z']),
                               (config.l515_x, config.l515_y, config.l515_z))
        xv, yv, zv = point_from_world_to_vc((xv, yv, zv), vc_world_coord)
        ret, msg = is_in_arena(xv, yv, zv, config.x_min, config.x_max, config.y_min, config.y_max, config.z_min,
                               config.z_max)
        if not ret:
            err = (f"error: is_in_arena failed, index:{keypoint['index']}, "
                   f"name:{KEYPOINT_INDEX_TO_NAME[keypoint['index']]}, "
                   f"before converted, x:{keypoint['x']}, y:{keypoint['y']}, z:{keypoint['z']}, "
                   f"after converted, x:{xv}, y:{yv}, z:{zv}")
            print(err)
            msg = msg + '---' + err
            return None, None, msg
        skeleton_data_in_pcl_coordinate_system.append(
            {'index': keypoint['index'], 'x': xv, 'y': yv, 'z': zv})
        skeleton_array.append([xv, yv, zv])
    # output matrix as well
    return skeleton_data_in_pcl_coordinate_system, np.array(skeleton_array), 'success'


def process_one_frame(pcl_file, sk_file, pcl_timestamp, posture, config, pos_idx, vc_id):
    if os.stat(pcl_file).st_size == 0:
        err_msg = f'error: 0kb point cloud file({pcl_file})'
        return False, err_msg

    pcl = read_pcl_from_txt(pcl_file)
    if pcl is None:
        err_msg = f'error: read none from pcl_file({pcl_file})'
        return False, err_msg

    sk_f = open(sk_file, 'r')
    json_data = json.load(sk_f)
    sk_f.close()

    targets_info, msg = generate_targets_info(json_data['gt_info'], posture, posture, config, pos_idx, vc_id)
    if targets_info is None:
        return False, msg

    point_cloud_info = {
        'timestamp': pcl_timestamp,
        'points': json.dumps(pcl),
        'gt_info': json.dumps(targets_info),
    }
    return True, point_cloud_info


def process(data, config, data_output_dir, id_str, label_str, pos_idx, vc_id, sensor_mounting,
            coord_convertion_log_output_folder):
    reporter = CoordConverterReporter()
    reporter.on_start(coord_convertion_log_output_folder,
                      create_collection_name(label_str, pos_idx, id_str, vc_id, sensor_mounting))

    for pcl_file, sk_file, pcl_timestamp, sk_timestamp in data:
        ret = process_one_frame(pcl_file, sk_file, pcl_timestamp, label_str, config, pos_idx, vc_id)
        if ret[0] is False:
            err_msg = ret[1]
            reporter.report(pcl_file, sk_file, float(pcl_timestamp), float(sk_timestamp), err_msg)
            continue

        output_f = open(f'{data_output_dir}/point_cloud_info_{pcl_timestamp}.json', 'w')
        json.dump(ret[1], output_f)
        output_f.close()

    reporter.on_finish()
