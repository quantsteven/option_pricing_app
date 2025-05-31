import numpy as np
from scipy.stats import norm
from typing import Union

from utils.flag_utils import cp2omega, get_touch_flag, get_barrier_flag


def european_option_payoff(
    option_type: str, S: float, K: float, T: float, r: float, q: float, sigma: float
) -> float:
    omega = cp2omega(option_type)
    return np.maximum(omega * (S - K), 0.0)


def european_option_bs_cf(
    option_type: str, S: float, K: float, T: float, r: float, q: float, sigma: float
) -> float:
    omega = cp2omega(option_type)
    discount = np.exp(-r * T)
    forward = S * np.exp((r - q) * T)
    moneyness = np.log(forward / K)
    vol_sqrt_time = sigma * np.sqrt(T)

    d1 = moneyness / vol_sqrt_time + 0.5 * vol_sqrt_time
    d2 = d1 - vol_sqrt_time

    return omega * discount * (forward * norm.cdf(omega * d1) - K * norm.cdf(omega * d2))


def single_touch_option_payoff(
    option_type: str, S: float, T: float, r: float, q: float, sigma: float, L: float, rbt: float = 1.0, PaE: bool = True
) -> float:
    is_down, touch = get_touch_flag(option_type)
    hit = (is_down * (S - L) <= 0)
    payoff = rbt * hit if touch else rbt * (1 - hit)
    return payoff


def single_touch_option_bs_cf(
    option_type: str, S: float, T: float, r: float, q: float, sigma: float, L: float, rbt: float = 1.0, PaE: bool = True
) -> float:
    if rbt == 0.0:
        return 0.0

    eta, touch = get_touch_flag(option_type)

    mu, v = (r - q) / sigma ** 2 - 0.5, sigma * np.sqrt(T)
    lbd = np.sqrt(mu ** 2 + 2 * np.maximum(0, r) / sigma ** 2)
    dfr = np.exp(-r * T)

    if touch:  # For touch option, get rebate when hitting barrier, can be PaE oe PaH

        if PaE:
            z = np.log(L / S) / v + mu * v
            val = rbt * dfr * ((L / S) ** (2 * mu) * norm.cdf(eta * z) + norm.cdf(eta * (z - 2 * mu * v)))
        else:
            z = np.log(L / S) / v + lbd * v
            val = rbt * ((L / S) ** (mu + lbd) * norm.cdf(eta * z) + (L / S) ** (mu - lbd) * norm.cdf(
                eta * (z - 2 * lbd * v)))

    else:  # For no-touch option, get rebate when not hitting barrier, must be PaE
        (x, y) = (np.log(S / L) / v + (1 + mu) * v, np.log(L / S) / v + (1 + mu) * v)
        val = rbt * dfr * (norm.cdf(eta * (x - v)) - (L / S) ** (2 * mu) * norm.cdf(eta * (y - v)))

    # SPECIAL HANDLING: when spot hits barrier at t = 0
    hit = eta * (S - L) <= 0

    if hit:
        val = rbt * np.exp(-r * PaE * T) if touch else 0

    return val


def val_rbt(R, PaE, T, mu_hat, mu_prime, sigma, xl, xh, du_flag, x, DFr):
    if PaE:
        return R * DFr * G(T, mu_hat, sigma, xl, xh, du_flag, x)
    else:
        return R * np.exp((mu_hat - mu_prime) * x / sigma ** 2) * G(T, mu_prime, sigma, xl, xh, du_flag, x)


def G(t, mu, sigma, xl, xh, du_flag, x):
    (k1, k2) = (np.arange(0, 7), np.arange(-6, 0))
    # (k1, k2) = (np.arange(0,30), np.arange(-29,0))

    if np.isscalar(x):
        (u1, u2) = (du_flag * x + 2 * k1 * (xh - xl), du_flag * x + 2 * k2 * (xh - xl))
    else:
        (u1, u2) = (du_flag * x + 2 * np.outer(k1, xh - xl), du_flag * x + 2 * np.outer(k2, xh - xl))

    (v, c) = (sigma * np.sqrt(t), mu / sigma ** 2)
    (e1, e2) = (np.exp(c * u1), np.exp(c * u2))
    PI1 = norm.cdf((-u1 - mu * t) / v) * e1 + norm.cdf((-u1 + mu * t) / v) / e1
    PI2 = norm.cdf((u2 + mu * t) / v) * e2 + norm.cdf((u2 - mu * t) / v) / e2

    if np.isscalar(x):
        return (np.sum(PI1) - np.sum(PI2)) * np.exp(c * x)
    else:
        return (np.sum(PI1, axis=0) - np.sum(PI2, axis=0)) * np.exp(c * x)


def double_touch_option_payoff(
    option_type: str, S: float, T: float, r: float, q: float, sigma: float, Ll: float, Lh: float,
    rbt: Union[float, list[float]] = 1.0, PaE: Union[bool, list[bool]] = True
) -> float:
    hit_lb, hit_ub = (S <= Ll), (S >= Lh)
    payoff = rbt * hit_lb if option_type.upper() == "OTDNTU" \
        else rbt * hit_ub if option_type.upper() == "OTUNTD" \
        else rbt[0] * hit_lb + rbt[1] * hit_ub if option_type.upper() == "DOT" \
        else rbt * (1 - hit_ub - hit_lb)
    return payoff


def double_touch_option_bs_cf(
    option_type: str, S: float, T: float, r: float, q: float, sigma: float, Ll: float, Lh: float,
    rbt: Union[float, list[float]] = 1.0, PaE: Union[bool, list[bool]] = True
) -> float:
    option_type = option_type.upper()
    dfr = np.exp(-r * T)
    mu_hat = (r - q) - sigma ** 2 / 2
    mu_prime = np.sqrt(mu_hat ** 2 + 2 * r * sigma ** 2)

    (xl, xh) = (np.log(Ll / S), np.log(Lh / S))

    # SPECIAL HANDLING: when spot hits barrier at t = 0
    hit_lb, hit_ub = (S <= Ll), (S >= Lh)

    if option_type == 'OTUNTD':
        val = rbt * np.exp(-r * PaE * T) if hit_ub else 0 if hit_lb else \
                val_rbt(rbt, PaE, T, mu_hat, mu_prime, sigma, xl, xh, 1, xh, dfr)

    elif option_type == 'OTDNTU':
        val = rbt * np.exp(-r * PaE * T) if hit_lb else 0 if hit_ub else \
                val_rbt(rbt, PaE, T, mu_hat, mu_prime, sigma, xl, xh, -1, xl, dfr)

    elif option_type == 'DOT':
        otd_ntu = double_touch_option_bs_cf('OTDNTU', S, T, r, q, sigma, Ll, Lh, rbt[0], PaE[0])
        otu_ntd = double_touch_option_bs_cf('OTUNTD', S, T, r, q, sigma, Ll, Lh, rbt[1], PaE[1])
        val = otu_ntd + otd_ntu

    else:  # DNT
        dot = double_touch_option_bs_cf('DOT', S, T, r, q, sigma, Ll, Lh, [rbt, rbt], [True, True])
        val = rbt * dfr - dot

    return val


def get_barrier_para(
    option_flag: list[int], S: float, K: float, T: float, r: float, b: float, sigma: float, L: float,
    rbt: float = 1.0, PaE: bool = True
) -> tuple:
    (eta, phi) = (option_flag[0], option_flag[2])
    (mu, v) = (b / sigma ** 2 - 0.5, sigma * np.sqrt(T))
    lbd = np.sqrt(mu ** 2 + 2 * np.maximum(0, r) / sigma ** 2)

    (x1, x2) = (np.log(S / K) / v + (1 + mu) * v, np.log(S / L) / v + (1 + mu) * v)
    (y1, y2) = (np.log(L ** 2 / (S * K)) / v + (1 + mu) * v, np.log(L / S) / v + (1 + mu) * v)
    (dfr, dfq) = (np.exp(-r * T), np.exp((b - r) * T))
    (M1, M2, LS) = (phi * S * dfq, phi * K * dfr, L / S)

    I1 = M1 * norm.cdf(phi * x1) - M2 * norm.cdf(phi * (x1 - v))
    I2 = M1 * norm.cdf(phi * x2) - M2 * norm.cdf(phi * (x2 - v))
    I3 = M1 * LS ** (2 * (mu + 1)) * norm.cdf(eta * y1) - M2 * LS ** (2 * mu) * norm.cdf(eta * (y1 - v))
    I4 = M1 * LS ** (2 * (mu + 1)) * norm.cdf(eta * y2) - M2 * LS ** (2 * mu) * norm.cdf(eta * (y2 - v))

    if rbt == 0.0:
        (I5, I6) = (0.0, 0.0)
    else:
        I5 = rbt * dfr * (
                norm.cdf(eta * (x2 - v)) - LS ** (2 * mu) * norm.cdf(eta * (y2 - v)))  # Pay-at-expiry for not KI
        if PaE:
            z = np.log(L / S) / v + mu * v
            I6 = rbt * dfr * (LS ** (2 * mu) * norm.cdf(eta * z) + norm.cdf(eta * (z - 2 * mu * v)))
        else:
            z = np.log(L / S) / v + lbd * v
            I6 = rbt * (LS ** (mu + lbd) * norm.cdf(eta * z) + LS ** (mu - lbd) * norm.cdf(eta * (z - 2 * lbd * v)))

    return I1, I2, I3, I4, I5, I6


def single_barrier_option_payoff(
    option_type: str, S: float, K: float, T: float, r: float, q: float, sigma: float, L: float,
    rbt: float = 1.0, PaE: bool = True
) -> float:
    is_down, knockout, _ = get_barrier_flag(option_type)
    hit = is_down * (S - L) <= 0
    if (knockout & hit) or (~knockout & ~hit):  # Rebate under two cases: 1. knock-out and hit, 2. knock-in and no hit
        payoff = rbt
    else:
        payoff = european_option_payoff(option_type[-1], S, K, T, r, q, sigma)
    return payoff


def single_barrier_option_bs_cf(
    option_type: str, S: float, K: float, T: float, r: float, q: float, sigma: float, L: float,
    rbt: float = 1.0, PaE: bool = True
) -> float:
    option_flag = get_barrier_flag(option_type)
    (I1, I2, I3, I4, I5, I6) = get_barrier_para(option_flag, S, K, T, r, r - q, sigma, L, rbt, PaE)

    (eta, knockout, omega) = (option_flag[0], option_flag[1], option_flag[2])
    (hit, K_L) = (eta * (S - L) <= 0, eta * (K - L) > 0)

    dc_and_up = (eta * omega == 1)  # Down Call and Up Put

    if knockout:  # Knock-Out: DOC, UOC, DOP, UOP
        v_no_hit = (I1 - I3 + I6 if K_L else I2 - I4 + I6) if dc_and_up else (I1 - I2 + I3 - I4 + I6 if K_L else I6)
        v_hit = rbt * np.exp(-r * T * PaE)

    else:  # Knock-In:  DIC, UIC, DIP, UIP
        v_no_hit = (I3 + I5 if K_L else I1 - I2 + I4 + I5) if dc_and_up else (I2 - I3 + I4 + I5 if K_L else I1 + I5)
        v_hit = european_option_bs_cf(option_type[-1], S, K, T, r, q, sigma)

    # SPECIAL HANDLING: when spot hits barrier at t = 0
    val = v_hit if hit else v_no_hit
    return val


def f(m, s, xl, xh, nu, z1, z2):
    k = np.arange(-6, 7)
    if np.isscalar(xl):
        (u, a1, a2, c) = (2 * k * (xh - xl), np.maximum(z1, xl), np.minimum(z2, xh), m / s ** 2)
    else:
        (u, a1, a2, c) = (2 * np.outer(k, xh - xl), np.maximum(z1, xl), np.minimum(z2, xh), m / s ** 2)

    yvet = np.exp(-c * u) * PHI(a1, a2, -m + u, s, nu) - np.exp(c * (2 * xh - u)) * PHI(a1, a2, -m - 2 * xh + u, s, nu)
    return np.sum(yvet) if np.isscalar(xl) else np.sum(yvet, axis=0)


def PHI(a1, a2, b, s, nu):
    return np.exp(0.5 * (nu * s) ** 2 - nu * b) * (norm.cdf(nu * s - (b + a1) / s) - norm.cdf(nu * s - (b + a2) / s))


def double_barrier_option_payoff(
    option_type: str, S: float, K: float, T: float, r: float, q: float, sigma: float, Ll: float, Lh: float,
    rbt: Union[float, list[float]] = 1.0, PaE: Union[bool, list[bool]] = True
) -> float:
    hit_lb, hit_ub = (S <= Ll), (S >= Lh)
    eo_payoff = european_option_payoff(option_type[-1], S, K, T, r, q, sigma)
    knockout = option_type[2].upper() == "O"
    if knockout:
        payoff = rbt[0] if hit_lb else rbt[1] if hit_ub else eo_payoff
    else:
        payoff = rbt if (~hit_lb & ~hit_ub) else eo_payoff
    return payoff


def double_barrier_option_bs_cf(
    option_type: str, S: float, K: float, T: float, r: float, q: float, sigma: float, Ll: float, Lh: float,
    rbt: Union[float, list[float]] = 1.0, PaE: Union[bool, list[bool]] = True
) -> float:
    dfr = np.exp(-r * T)

    # SPECIAL HANDLING: when spot hits barrier at t = 0
    hit_lb, hit_ub = (S <= Ll), (S >= Lh)

    if option_type[2].upper() == 'I':  # KI, use barrier parity
        v_euro = european_option_bs_cf(option_type[-1], S, K, T, r, q, sigma)
        option_type = str.replace(option_type, 'I', 'O')
        v_ko = double_barrier_option_bs_cf(option_type, S, K, T, r, q, sigma, Ll, Lh, [rbt, rbt], [True, True])
        return v_euro - v_ko + rbt * dfr

    else:
        (lR, uR, lPaE, uPaE) = (rbt[0], rbt[1], PaE[0], PaE[1])

        mu_hat = (r - q) - sigma ** 2 / 2
        mu_prime = np.sqrt(mu_hat ** 2 + 2 * r * sigma ** 2)

        (x0, xl, xh) = (np.log(K / S), np.log(Ll / S), np.log(Lh / S))

        if option_type[-1].upper() in ("C", "CALL"):
            val = S * f(mu_hat * T, sigma * np.sqrt(T), xl, xh, 1, x0, xh) \
                  - K * f(mu_hat * T, sigma * np.sqrt(T), xl, xh, 0, x0, xh)
        else:
            val = K * f(mu_hat * T, sigma * np.sqrt(T), xl, xh, 0, xl, x0) \
                  - S * f(mu_hat * T, sigma * np.sqrt(T), xl, xh, 1, xl, x0)

        val = dfr * val \
              + val_rbt(lR, lPaE, T, mu_hat, mu_prime, sigma, xl, xh, -1, xl, dfr) \
              + val_rbt(uR, uPaE, T, mu_hat, mu_prime, sigma, xl, xh, 1, xh, dfr)

        return uR * np.exp(-r * T * uPaE) if hit_ub else lR * np.exp(-r * T * lPaE) if hit_lb else val


def european_option_heston_cf(
    option_type: str, S: float, K: float, T: float, r: float, q: float, sigma: float
) -> float:
    return 0.0
