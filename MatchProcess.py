from Config import Config
from CoordinatesConverter import d455_to_vayyar_care
from Tool import *


def match(skeleton_data_folder: str, pcl_data_folder: str, output_dir, config):
    skeleton_files = get_files_list(skeleton_data_folder, get_timestamp_ms_in_skeleton_filename)
    pcl_files = get_files_list(pcl_data_folder, get_timestamp_ms_in_pcl_filename)

    # csv_file = open(f'generated_at_{datetime.now().strftime("%Y%m%d-%H%M%S")}.csv', 'w', newline='')
    # csv_writer = csv.writer(csv_file)
    # csv_writer.writerow(['pcl_filename', 'sk_filename', 'pcl_timestamp', 'sk_timestamp'])

    matched_data_list = []

    skeleton_file_pointer = 0
    for pcl_filename, pcl_timestamp in pcl_files:
        while True:
            sk_filename, sk_timestamp = skeleton_files[skeleton_file_pointer]
            if sk_timestamp < pcl_timestamp:
                skeleton_file_pointer += 1
            else:
                break
        # csv_writer.writerow([pcl_filename, sk_filename, str(pcl_timestamp), str(sk_timestamp)])
        matched_data_list.append(
            [os.path.join(pcl_data_folder, pcl_filename), os.path.join(skeleton_data_folder, sk_filename),
             str(pcl_timestamp), str(sk_timestamp)])

    # csv_file.close()

    process(matched_data_list, config, output_dir)


def generate_target_info(skeleton_json, posture, action, config):
    skeleton_in_vc_coord_system, skeleton_mat = covert_skeleton_to_vc_coordinate_system(skeleton_json, config)
    if skeleton_in_vc_coord_system is None:
        return None
    target_info = {
        'posture': posture,
        'action': action,
        'isfall': 'no',
        'skeleton': skeleton_in_vc_coord_system,
        'bbox': get_bbox(skeleton_mat)
    }
    return target_info


def generate_targets_info(targets_json, posture, action, config):
    targets_info = []
    for target in targets_json:
        target_info = generate_target_info(target['skeleton'], posture, action, config)
        if target_info is None:
            return None
        targets_info.append(target_info)
    return targets_info


def covert_skeleton_to_vc_coordinate_system(skeleton_json, config):
    skeleton_data_in_pcl_coordinate_system = []
    skeleton_array = []
    for keypoint in skeleton_json:
        xv, yv, zv = d455_to_vayyar_care(keypoint['x'], keypoint['y'], keypoint['z'],
                                         config.d455_x, config.d455_y, config.d455_z)
        if not is_in_arena(xv, yv, zv, config.x_min, config.x_max, config.y_min, config.y_max, config.z_min,
                           config.z_max):
            print(f"error: is_in_arena failed, index:{keypoint['index']}, "
                  f"before converted, x:{keypoint['x']}, y:{keypoint['y']}, z:{keypoint['z']}, "
                  f"after converted, x:{xv}, y:{yv}, z:{zv}")
            return None, None
        skeleton_data_in_pcl_coordinate_system.append(
            {'index': keypoint['index'], 'x': xv, 'y': yv, 'z': zv})
        skeleton_array.append([xv, yv, zv])
    # output matrix as well
    return skeleton_data_in_pcl_coordinate_system, np.array(skeleton_array)


def process(data, config, output_dir):
    for pcl_file, sk_file, pcl_timestamp, sk_timestamp in data:
        point_cloud_info = {'timestamp': pcl_timestamp}
        pcl = read_pcl_from_txt(pcl_file)
        if pcl is None:
            continue
        point_cloud_info['points'] = json.dumps(pcl)

        sk_f = open(sk_file, 'r')
        json_data = json.load(sk_f)
        sk_f.close()

        people_count = len(json_data['gt_info'])
        if people_count < 2:
            print(f'error: should more than 1 people, but only {people_count}')
            print('----------')
            continue

        posture, action = get_posture_and_action_label(os.path.basename(pcl_file))
        targets_info = generate_targets_info(json_data['gt_info'], posture, action, config)
        if targets_info is None:
            print(f'error: generate_targets_info failed, skeleton out of arena: {sk_file}')
            print('----------')
            continue
        point_cloud_info['gt_info'] = json.dumps(targets_info)

        output_f = open(f'{output_dir}/point_cloud_info_{pcl_timestamp}.json', 'w')
        json.dump(point_cloud_info, output_f)
        output_f.close()


if __name__ == '__main__':
    output_dir = make_output_dir()
    match(r'C:\Users\XiuzhuJian_05qqcw2\PycharmProjects\D455Test\output\20240711-1609',
          r'C:\jxz\PycharmProjects\VayyarCareDataCollector\console\data\2024-07-11-lab-YZX\Wall-vc1-ip-192.168.8.41\walk-30-s_4_20240711-1609',
          output_dir,
          Config(0, 0, 0.78, -1.5, 1.5, 0.2, 3, 0, 1.8))
