def get_timestamp_ms_in_skeleton_filename(filename: str):
    if not (filename.startswith('skeleton_data_') and filename.endswith('.json')):
        print(f'error filename: {filename}')
        return -1
    return float(filename.rsplit('_', 1)[-1].rsplit('.', 1)[0])
