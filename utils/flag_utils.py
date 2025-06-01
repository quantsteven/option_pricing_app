
def cp2omega(option_type: str) -> int:
    return 1 if option_type.upper() in ("C", "CALL") else -1  # call = 1, put = -1


def get_touch_flag(option_type: str) -> list[int]:
    flag = [
        1 if option_type[2].upper() == 'D' else -1,   # down = 1,  up = -1
        1 if option_type[:2].upper() == 'OT' else 0   # touch = 1, no-touch = 0
    ]
    return flag


def get_barrier_flag(option_type: str) -> list[int]:
    flag = [
        1 if option_type[0].upper() == 'D' else -1,   # down = 1,      up = -1
        1 if option_type[1].upper() == 'O' else -1,   # knock-out = 1, knock-in = -1
        1 if option_type[2].upper() == 'C' else -1    # call = 1,      put = -1
    ]
    return flag
