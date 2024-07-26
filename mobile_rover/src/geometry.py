import math


def normalize_th_pi(angle):
    """
    Normalize an angle to be between -pi and pi
    """
    return (angle + math.pi) % (2 * math.pi) - math.pi


def normalize_th_2pi(angle):
    """
    Normalize an angle to be between 0 and 2pi
    """
    return (angle + 2 * math.pi) % (2 * math.pi)
