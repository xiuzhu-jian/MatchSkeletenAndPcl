import json
import os
from pathlib import Path

from Definitions.Config import Config
from CoordConvertion.L515Coord import stand_pos_idx_to_l515_coord, sit_pos_idx_to_l515_coord
from MatchProcess import match
from NameParser.PclDataFolderNameParser import parse_pcl_data_folder_name
from NameParser.PclDataFileNameParser import parse_arena
from Tools.FolderCreater import create_data_output_folder, create_match_log_output_folder, \
    create_coord_convertion_log_output_folder, create_output_folder, create_match_output_folder
from NameParser.VCFolderNameParser import parse_vc_folder_name


def main():
    output_folder = create_output_folder()
    data_folder = create_data_output_folder(output_folder)
    match_log_output_folder = create_match_log_output_folder(output_folder)
    coord_convertion_log_output_folder = create_coord_convertion_log_output_folder(output_folder)

    with open('ConfigData/config.json', 'r') as f:
        config_data = json.load(f)

        pcl_skeleton_data_folders = []
        for item in config_data:
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
                            sensor_mounting,
                        )
                    )

        total = len(pcl_skeleton_data_folders)
        for index, (pcl_data_folder,
                    skeleton_data_folder,
                    config,
                    collection_id,
                    posture,
                    pos_idx,
                    vc_id,
                    sensor_mounting) in enumerate(pcl_skeleton_data_folders):
            print(f'progress: {index + 1}/{total}\r\n{pcl_data_folder}\r\n{skeleton_data_folder}')

            generated_data_folder_fullpath = create_match_output_folder(data_folder, posture, pos_idx, collection_id,
                                                                        vc_id, sensor_mounting)

            match(skeleton_data_folder,
                  pcl_data_folder,
                  generated_data_folder_fullpath,
                  match_log_output_folder,
                  coord_convertion_log_output_folder,
                  collection_id,
                  posture,
                  config,
                  pos_idx,
                  vc_id,
                  sensor_mounting)


if __name__ == '__main__':
    main()
