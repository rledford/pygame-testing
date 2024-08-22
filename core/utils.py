def clamp(v: int | float, min_v: int | float, max_v: int | float):
    return max(min_v, min(max_v, v))


def sign(v: int | float):
    if v < 0:
        return -1
    if v > 0:
        return 1
    return 0
