import json


def create_final_data(timestamp_ms: float,
                      points: list,
                      posture: str,
                      action: str,
                      isfall: str,
                      skeleton: list,
                      bbox: dict):
    gt_info = [{
        'posture': posture,
        'action': action,
        'isfall': isfall,
        'skeleton': skeleton,
        'bbox': bbox,
    }]
    data = {
        'timestamp': timestamp_ms,
        'points': json.dumps(points),
        'gt_info': json.dumps(gt_info),
    }
    return data
