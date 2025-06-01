
def fod(y1: float, y_1: float, a: float) -> float:
    # first order difference
    return (y1 - y_1) / a


def sod(y1: float, y0: float, y_1: float, a: float) -> float:
    # second order difference
    return (y1 - 2 * y0 + y_1) / (a ** 2)


def somd(y11: float, y1_1: float, y_11: float, y_1_1: float, a: float, b: float) -> float:
    # second order mixed difference
    return (y11 - y1_1 - y_11 + y_1_1) / (4 * a * b)


def tod(y2: float, y1: float, y0: float, y_1: float, a: float) -> float:
    # third order difference
    return (y2 - 3 * y1 + 3 * y0 - y_1) / a ** 3


def tomd(y11: float, y01: float, y_11: float, y1_1: float, y0_1: float, y_1_1: float, a: float, b: float) -> float:
    # third order mixed difference
    return (y11 - 2 * y01 + y_11 - y1_1 + 2 * y0_1 - y_1_1) / (2 * a ** 2 * b)
