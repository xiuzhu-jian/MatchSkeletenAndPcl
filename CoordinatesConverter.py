def d455_to_vayyar_care(x, y, z, d455_x, d455_y, d455_z):
    """
    convert coordinates from D455's coordinate system to Vayyar Care
    Args:
        x: right with rgb camera as origin
        y: down with rgb camera as origin
        z: depth
        d455_x: d455 coordinate x in vayyar care coordinate system
        d455_y: d455 coordinate y in vayyar care coordinate system
        d455_z: d455 coordinate z in vayyar care coordinate system

    Returns:
        coordinates in Vayyar Care's coordinate system
    """
    xv = -d455_x + x
    yv = d455_y + z
    zv = -(-d455_z + y)
    return xv, yv, zv
