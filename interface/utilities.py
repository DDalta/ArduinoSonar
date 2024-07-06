from math import sin, cos, radians

def get_pos_from_angle(center, angle, radius):
    conv_angle = angle + 90
    return ((center[0] + sin(radians(conv_angle)) * radius), (center[1] + cos(radians(conv_angle)) * radius))