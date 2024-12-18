def parse_filename(filename: str):
    posture = filename.split('-', 1)[0]
    pos_idx, collection_id = filename.split('_')[1:]
    return posture, int(pos_idx), collection_id
