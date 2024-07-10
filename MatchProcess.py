from Config import config
from CoordinatesConverter import d455_to_vayyar_care
from Tool import *


def match(skeleton_data_folder: str, pcl_data_folder: str):
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
    return matched_data_list


def generate_target_info(skeleton_json, d455_x, d455_y, d455_z):
    target_info = {
        'posture': 'stand',
        'action': 'walk',
        'isfall': 'no',
        'skeleton': covert_skeleton_to_vc_coordinate_system(skeleton_json, d455_x, d455_y, d455_z),
        'bbox': get_bbox(convert_skeleton_json_to_matrix(skeleton_json))
    }
    return target_info


def covert_skeleton_to_vc_coordinate_system(skeleton_json, d455_x, d455_y, d455_z):
    skeleton_data_in_pcl_coordinate_system = []
    for keypoint in skeleton_json:
        xv, yv, zv = d455_to_vayyar_care(keypoint['x'], keypoint['y'], keypoint['z'],
                                         d455_x, d455_y, d455_z)
        skeleton_data_in_pcl_coordinate_system.append(
            {'index': keypoint['index'], 'x': xv, 'y': yv, 'z': zv})
    return skeleton_data_in_pcl_coordinate_system


def process(data):
    output_dir = make_output_dir()

    d455_x = config.d455_x
    d455_y = config.d455_y
    d455_z = config.d455_z
    for pcl_file, sk_file, pcl_timestamp, sk_timestamp in data:
        point_cloud_info = {'timestamp': pcl_timestamp}
        pcl = read_pcl_from_txt(pcl_file)
        if pcl is None:
            continue
        point_cloud_info['points'] = json.dumps(pcl)

        sk_f = open(sk_file, 'r')
        targets_info = []
        json_data = json.load(sk_f)
        sk_f.close()
        for target in json_data['gt_info']:
            targets_info.append(generate_target_info(target['skeleton'], d455_x, d455_y, d455_z))
        point_cloud_info['gt_info'] = json.dumps(targets_info)

        output_f = open(f'{output_dir}/point_cloud_info_{pcl_timestamp}.json', 'w')
        json.dump(point_cloud_info, output_f)
        output_f.close()


if __name__ == '__main__':
    matched = match(r'C:\Users\XiuzhuJian_05qqcw2\PycharmProjects\D455Test\output\20240709-1444',
                    r'C:\jxz\PycharmProjects\VayyarCareDataCollector\console\data\2024-07-09-lab-YZX\Wall-vc1-ip-192.168.8.41\Wash feet-30-s_7_20240709-1444')
    process(matched)
