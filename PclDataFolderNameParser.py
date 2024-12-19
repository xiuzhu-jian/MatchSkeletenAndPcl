def parse_pcl_data_folder_name(pcl_data_folder_name: str):
    posture = pcl_data_folder_name.split('-', 1)[0]
    pos_idx, collection_id = pcl_data_folder_name.split('_')[1:]
    return posture, int(pos_idx), collection_id
