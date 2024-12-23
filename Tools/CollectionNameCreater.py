def create_collection_name(posture, pos_idx, collection_id, vc_id, sensor_mounting):
    return f'{posture}_{pos_idx:02}_{collection_id}_{vc_id}_{sensor_mounting}'