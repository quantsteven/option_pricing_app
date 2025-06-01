import numpy as np
from utils.configs import GREEK_CONFIG
from utils.difference_utils import fod, sod
from utils.shock_utils import get_shock, scheme2weight, get_scaling_factor


def get_index(param: dict, dS: float) -> tuple[np.ndarray, np.ndarray]:
    i_left, i_right = np.array([]), np.array([])

    S0 = param["S"]
    checkpoints = ["L", "Ll", "Lh"]

    for chkpt in checkpoints:
        if chkpt in param.keys():
            C = param[chkpt]
            iL = np.where((np.abs(C - S0) <= dS) & (S0 <= C))[0]
            iR = np.where((np.abs(S0 - C) <= dS) & (S0 >= C))[0]
            i_left = np.concatenate((i_left, iL))
            i_right = np.concatenate((i_right, iR))

    return i_left.astype(int), i_right.astype(int)


class FDGreeks:

    def __init__(self, function: callable, parameter: dict):
        self.func = function
        self.param = parameter
        self.param_original = parameter.copy()

    def reset_param(self):
        self.param = self.param_original

    @property
    def delta(self):
        func, param = self.func, self.param.copy()
        setting = GREEK_CONFIG["delta"]
        S0 = param["S"]
        dS = get_shock(S0, setting)

        w = scheme2weight(setting["shock_mode"], order=1)
        w = np.tile(w, (len(S0), 1)) if not np.isscalar(S0) else w  # copy w len(S0) times

        i_left, i_right = get_index(param, dS)

        if np.isscalar(S0):  # S0 is a scalar
            # use backward difference scheme if spot is at LHS of barrier, w = [0,-1]
            # use forward difference is spot is at RHS of barrier, w = [1,0]
            w = [0, -1] if len(i_left) != 0 else [1, 0] if len(i_right) != 0 else w

            param["S"] = S0 + w[0] * dS
            V0 = func(**param)
            param["S"] = S0 + w[1] * dS
            V1 = func(**param)
            delta = fod(V0, V1, (w[0] - w[1]) * dS)

        else:  # S0 is an array
            # use backward difference scheme if spot is at LHS of barrier, update i_left row of w with [0,-1]
            # use forward difference is spot is at RHS of barrier, update i_right row of w with [1,0]
            if len(i_left) != 0:
                w[i_left, :] = [0, -1]
            if len(i_right) != 0:
                w[i_right, :] = [1, 0]

            param["S"] = S0 + w[:, 0] * dS
            V0 = func(**param)
            param["S"] = S0 + w[:, 1] * dS
            V1 = func(**param)
            delta = fod(V0, V1, (w[:, 0] - w[:, 1]) * dS)

        return delta

    @property
    def gamma(self):
        func, param = self.func, self.param.copy()
        setting = GREEK_CONFIG["gamma"]
        S0 = param["S"]
        dS = get_shock(S0, setting)

        w = scheme2weight(setting["shock_mode"], order=2)
        w = np.tile(w, (len(S0), 1)) if not np.isscalar(S0) else w  # copy w len(S0) times

        i_left, i_right = get_index(param, dS)

        if np.isscalar(S0):  # S0 is a scalar
            # use backward difference scheme if spot is at LHS of barrier, w = [0,-1]
            # use forward difference is spot is at RHS of barrier, w = [1,0]
            w = [0, -1, -2] if len(i_left) != 0 else [2, 1, 0] if len(i_right) != 0 else w

            param["S"] = S0 + w[0] * dS
            V0 = func(**param)
            param["S"] = S0 + w[1] * dS
            V1 = func(**param)
            param["S"] = S0 + w[2] * dS
            V2 = func(**param)

            gamma = sod(V0, V1, V2, (w[0] - w[1]) * dS)

        else:  # S0 is an array
            # use backward difference scheme if spot is at LHS of barrier, update i_left row of w with [0,-1,-2]
            # use forward difference is spot is at RHS of barrier, update i_right row of w with [2,1,0]
            if len(i_left) != 0:
                w[i_left, :] = np.array([0, -1, -2])
            if len(i_right) != 0:
                w[i_right, :] = np.array([2, 1, 0])

            param["S"] = S0 + w[:, 0] * dS
            V0 = func(**param)
            param["S"] = S0 + w[:, 1] * dS
            V1 = func(**param)
            param["S"] = S0 + w[:, 2] * dS
            V2 = func(**param)
            gamma = sod(V0, V1, V2, (w[:, 0] - w[:, 1]) * dS)

        return gamma

    @property
    def vega(self):
        func, param = self.func, self.param.copy()
        setting = GREEK_CONFIG["vega"]
        v0 = param["sigma"]
        dv = get_shock(v0, setting)
        w = scheme2weight(setting["shock_mode"], order=1)

        param["sigma"] = v0 + w[0] * dv
        V0 = func(**param)
        param["sigma"] = v0 + w[1] * dv
        V1 = func(**param)

        dvol = setting["shock_magnitude"] * get_scaling_factor(setting["shock_type"], setting["shock_unit"])
        return fod(V0, V1, (w[0] - w[1]) * dv) * dvol

    @property
    def theta(self):
        func, param = self.func, self.param.copy()
        setting = GREEK_CONFIG["theta"]
        T = param["T"]
        dT = get_shock(T, setting)

        V0 = func(**param)
        param["T"] = 1e-5 if T <= dT else T - dT
        V1 = func(**param)

        return -(V0 - V1)

    @property
    def rho(self):
        func, param = self.func, self.param.copy()
        setting = GREEK_CONFIG["rho"]
        r0 = param["r"]
        dr = get_shock(r0, setting)
        w = scheme2weight(setting["shock_mode"], order=1)

        param["r"] = r0 + w[0] * dr
        V0 = func(**param)
        param["r"] = r0 + w[1] * dr
        V1 = func(**param)

        dIR = 0.01
        return fod(V0, V1, (w[0] - w[1]) * dr) * dIR

    @property
    def volga(self):
        func, param = self.func, self.param.copy()
        setting = GREEK_CONFIG["volga"]
        v0 = param["sigma"]
        dv = get_shock(v0, setting)
        w = scheme2weight(setting["shock_mode"], order=2)

        param["sigma"] = v0 + w[0] * dv
        V0 = func(**param)
        param["sigma"] = v0 + w[1] * dv
        V1 = func(**param)
        param["sigma"] = v0 + w[2] * dv
        V2 = func(**param)

        dvol = setting["shock_magnitude"] * get_scaling_factor(setting["shock_type"], setting["shock_unit"])

        return sod(V0, V1, V2, (w[0] - w[1]) * dv) * dvol ** 2

    @property
    def vanna(self):
        func, param = self.func, self.param.copy()
        setting = GREEK_CONFIG["vanna"]
        v0 = param["sigma"]
        dv = get_shock(v0, setting)
        w = scheme2weight(setting["shock_mode"], order=2)

        self.param["sigma"] = v0 + w[0] * dv
        D0 = self.delta
        self.param["sigma"] = v0 + w[1] * dv
        D1 = self.delta

        dvol = setting["shock_magnitude"] * get_scaling_factor(setting["shock_type"], setting["shock_unit"])

        return fod(D0, D1, (w[0] - w[1]) * dv) * dvol
