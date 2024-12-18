from L515Coord import *
from PostureType import *
from VCCoord import *

X = 0
Y = 1
Z = 2

L515_POS_TYPE_FRONT = 0
L515_POS_TYPE_FRONT_LEFT = 1
L515_POS_TYPE_FRONT_RIGHT = 2
L515_POS_TYPE_BACK = 3

POS_TO_L515_POS_TYPE = {
    'stand:0,1,2,3,4,5,6,7': L515_POS_TYPE_BACK,
    'stand:8,9,10,11,12,13,14,15': L515_POS_TYPE_FRONT,
    'sit:1,2,5,6,8,9,10,11,12,13,14,15': L515_POS_TYPE_FRONT,
    'sit:0,7': L515_POS_TYPE_FRONT_LEFT,
    'sit:3,4': L515_POS_TYPE_FRONT_RIGHT,
}


def convert_skeleton_to_vc_coord_system(skeleton_coords: list, pos_idx: int, vc_id: int, posture_type: PostureType):
    """
    skeleton L515 -> world -> vc
    """
    if posture_type == PostureType.STAND:
        l515_coord = stand_pos_idx_to_l515_coord(pos_idx)
    elif posture_type == PostureType.SIT:
        l515_coord = sit_pos_idx_to_l515_coord(pos_idx)
    else:
        print('posture_type must be STAND, SIT')
        return

    # Determine the appropriate converter based on the position of the L515.
    if posture_type == PostureType.STAND and pos_idx_to_row_idx(pos_idx) in (0, 1):
        converter = front_l515_to_world
    else:
        converter = back_l515_to_world

    # convert from L515 coord system to world coord system
    skeleton_vc_coords = []
    vc_world_coord = VC_ID_TO_COORD[vc_id]
    for skeleton_coord in skeleton_coords:
        skeleton_world_coord = converter(skeleton_coord, l515_coord)
        skeleton_vc_coord = world_to_vc(skeleton_world_coord, vc_world_coord)
        skeleton_vc_coords.append(skeleton_vc_coord)

    return skeleton_vc_coords


def front_l515_to_world(l515_point_coord, l515_world_coord):
    new_x = l515_point_coord[X] + l515_world_coord[X]
    new_y = l515_point_coord[Z] + l515_world_coord[Y]
    new_z = l515_world_coord[Z] - l515_point_coord[Y]
    return new_x, new_y, new_z

def back_l515_to_world(l515_point_coord, l515_world_coord):
    new_x = -l515_point_coord[X] + l515_world_coord[X]
    new_y = -l515_point_coord[Z] + l515_world_coord[Y]
    new_z = l515_world_coord[Z] - l515_point_coord[Y]
    return new_x, new_y, new_z

def world_to_vc(world_coord, vc_world_coord):
    new_x = world_coord[X] - vc_world_coord[X]
    new_y = world_coord[Y] - vc_world_coord[Y]
    new_z = world_coord[Z]
    return new_x, new_y, new_z