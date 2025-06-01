
def scheme2weight(scheme: str, order: int) -> list:
    scheme = scheme.lower()
    forward_scheme = scheme in ('f', 'fwd', 'forward', 'u', 'up')
    center_scheme = scheme in ('c', 'center', 'centred', 'central')
    backward_scheme = scheme in ('b', 'bwd', 'backward', 'd', 'down')

    if order == 1:
        w = [1, 0] if forward_scheme else [1, -1] if center_scheme else [0, -1]
    elif order == 2:
        w = [2, 1, 0] if forward_scheme else [1, 0, -1] if center_scheme else [0, -1, -2]
    else:
        w = []
    return w


def get_scaling_factor(shock_type: str = "abs", shock_unit: str = "bp") -> float:
    shock_type, shock_unit = shock_type.lower(), shock_unit.lower()
    absolute_shock = "abs" in shock_type
    percent_labels = ["%", "percentage", "percent"]
    basis_point_labels = ["bp", "bps", "basis point", "basis points"]

    if absolute_shock:  # the rate normally in unit of %
        scaling_factor = 0.01 if shock_unit in percent_labels \
            else 0.0001 if shock_unit in basis_point_labels else 1.0
    else:  # relative shock, a% means X*(1+0.01a)
        scaling_factor = 0.01 if shock_unit in percent_labels else 1.0

    return scaling_factor


def get_change(x: float, shock_type: str, shock_magnitude: float) -> float:
    return shock_magnitude if "abs" in shock_type.lower() else shock_magnitude * x


def get_shock(x: float, setting: dict) -> float:
    shock_type, shock_magnitude, shock_unit = setting["shock_type"], setting["shock_magnitude"], setting["shock_unit"]
    s = get_scaling_factor(shock_type, shock_unit)
    dx = get_change(x, shock_type, shock_magnitude * s)
    return dx
