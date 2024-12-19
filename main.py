import json
import os
from pathlib import Path

from Config import Config
from L515Coord import stand_pos_idx_to_l515_coord, sit_pos_idx_to_l515_coord
from MatchProcess import match
from PclDataFolderNameParser import parse_pcl_data_folder_name
from PointCloudDataFileNameParser import parse_arena
from Tool import make_output_dir
from VCFolderNameParser import parse_vc_folder_name

output_to_one_folder = False

if __name__ == '__main__':
    if output_to_one_folder:
        output_dir = make_output_dir()
    else:
        output_dir = None

    with open('ConfigData/config.json', 'r') as f:
        config = json.load(f)

        pcl_skeleton_data_folders = []
        for item in config:
            for vc_dir in os.listdir(item['pcl_all_data_folder']):
                sensor_mounting, vc_id = parse_vc_folder_name(vc_dir)
                for pcl_data_dir in os.listdir(os.path.join(item['pcl_all_data_folder'], vc_dir)):
                    posture, pos_idx, collection_id = parse_pcl_data_folder_name(pcl_data_dir)

                    pcl_data_dir_fullpath = os.path.join(item['pcl_all_data_folder'], vc_dir, pcl_data_dir)
                    for pcl_data_file in Path(pcl_data_dir_fullpath).iterdir():
                        if pcl_data_file.is_file():
                            break

                    arena: list = parse_arena(pcl_data_file.name)

                    if posture == 'stand':
                        l515_coord = stand_pos_idx_to_l515_coord(pos_idx)
                    elif posture == 'sit':
                        l515_coord = sit_pos_idx_to_l515_coord(pos_idx)
                    else:
                        print(f'posture_type must be STAND, SIT, exit, pcl_data_dir_fullpath: {pcl_data_dir_fullpath}')
                        exit(1)

                    config = Config(*l515_coord, *arena)

                    pcl_skeleton_data_folders.append(
                        (
                            pcl_data_dir_fullpath,
                            os.path.join(item['skeleton_data_folder'], collection_id),
                            config,
                            collection_id,
                            posture,
                            pos_idx,
                            vc_id,
                        )
                    )

        total = len(pcl_skeleton_data_folders)
        for index, (pcl_data_folder,
                    skeleton_data_folder,
                    config,
                    collection_id,
                    posture,
                    pos_idx,
                    vc_id) in enumerate(pcl_skeleton_data_folders):
            print(f'progress: {index + 1}/{total}\r\n{pcl_data_folder}\r\n{skeleton_data_folder}')
            match(skeleton_data_folder,
                  pcl_data_folder,
                  output_dir,
                  collection_id,
                  posture,
                  config,
                  pos_idx,
                  vc_id)
