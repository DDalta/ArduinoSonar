from math import sin, cos, radians

def get_pos_from_angle(center, angle, radius):
    conv_angle = angle + 90
    return ((center[0] + sin(radians(conv_angle)) * radius), (center[1] + cos(radians(conv_angle)) * radius))

def get_pos_from_distance(distance, max_distance, center, radius):
    # 40 -> 0
    # (center.y - radius) -> center.y
    # https://stackoverflow.com/questions/345187/math-mapping-numbers
    ratio = ((center[1] - radius) - center[1]) / max_distance
    return distance * ratio + center[1]