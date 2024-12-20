import csv

from Definitions.Config import Config
from CoordConvertion.CoordConverter import point_from_front_l515_to_world, point_from_back_l515_to_world, \
    point_from_world_to_vc
from Reporters.CoordConvertionReporter import CoordConverterReporter
from CoordConvertion.L515Coord import pos_idx_to_row_idx
from Definitions.SkeletonDef import KEYPOINT_INDEX_TO_NAME
from Tools.TimeTool import ms_timestamp_to_str
from Tools.Tool import *
from CoordConvertion.VCCoord import VC_ID_TO_COORD

X_CORRECTION_IN_METERS = 0.25
LABEL_TIMESTAMP_CORRECTION_IN_MILLISECONDS = 0


def match(skeleton_data_folder: str, pcl_data_folder: str, output_dir, id_str, label_str, config, pos_idx, vc_id,
          sensor_mounting):
    skeleton_files = get_files_list(skeleton_data_folder, get_timestamp_ms_in_skeleton_filename)
    pcl_files = get_files_list(pcl_data_folder, get_timestamp_ms_in_pcl_filename)

    csv_file = open(f'RunData/generated_at_{datetime.now().strftime("%Y%m%d-%H%M%S")}_{id_str}.csv', 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(
        ['pcl_filename', 'sk_filename', 'pcl_timestamp_ms', 'sk_timestamp_ms', 'pcl_time', 'sk_time', 'diff_ms'])

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

        csv_writer.writerow([pcl_filename, sk_filename, f'[{pcl_timestamp}]', f'[{sk_timestamp}]',
                             f'[{ms_timestamp_to_str(pcl_timestamp)}]', f'[{ms_timestamp_to_str(sk_timestamp)}]',
                             f'{pcl_timestamp - sk_timestamp}'])
        matched_data_list.append(
            [os.path.join(pcl_data_folder, pcl_filename),
             os.path.join(skeleton_data_folder, sk_filename),
             str(pcl_timestamp),
             str(sk_timestamp)])

    csv_file.close()

    process(matched_data_list, config, output_dir, id_str, label_str, pos_idx, vc_id, sensor_mounting)


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
                               (config.d455_x, config.d455_y, config.d455_z))
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


def process(data, config, output_dir, id_str, label_str, pos_idx, vc_id, sensor_mounting):
    reporter = CoordConverterReporter()
    reporter.on_start(f'{label_str}_{pos_idx:02}_{id_str}_{vc_id}_{sensor_mounting}')
    fail_count = 0
    total = len(data)
    for pcl_file, sk_file, pcl_timestamp, sk_timestamp in data:
        point_cloud_info = {'timestamp': pcl_timestamp}

        sk_f = open(sk_file, 'r')
        json_data = json.load(sk_f)
        sk_f.close()

        if os.stat(pcl_file).st_size == 0:
            print(f'error: 0kb point cloud file({pcl_file})')
            reporter.report(pcl_file, sk_file, float(pcl_timestamp), float(sk_timestamp), '0kb pcl')
            continue

        pcl = read_pcl_from_txt(pcl_file)
        if pcl is None:
            print(f'error: read none from pcl_file({pcl_file})')
            reporter.report(pcl_file, sk_file, float(pcl_timestamp), float(sk_timestamp), 'none pcl')
            continue
        point_cloud_info['points'] = json.dumps(pcl)

        targets_info, msg = generate_targets_info(json_data['gt_info'], label_str, label_str, config, pos_idx, vc_id)
        if targets_info is None:
            fail_count += 1
            print(f'error: generate_targets_info failed, skeleton out of arena: {sk_file}')
            print(f'fail_count:{fail_count}, total:{total}----------')
            reporter.report(pcl_file, sk_file, float(pcl_timestamp), float(sk_timestamp), msg)
            continue
        point_cloud_info['gt_info'] = json.dumps(targets_info)

        output_f = open(f'{output_dir}/point_cloud_info_{pcl_timestamp}.json', 'w')
        json.dump(point_cloud_info, output_f)
        output_f.close()

    reporter.on_finish()


if __name__ == '__main__':
    output_dir = make_output_dir()
    match(r'C:\Users\XiuzhuJian_05qqcw2\PycharmProjects\D455Test\output\20240711-1609',
          r'C:\jxz\PycharmProjects\VayyarCareDataCollector\console\data\2024-07-11-lab-YZX\Wall-vc1-ip-192.168.8.41\walk-30-s_4_20240711-1609',
          output_dir,
          Config(0, 0, 0.78, -1.5, 1.5, 0.2, 3, 0, 1.8))
