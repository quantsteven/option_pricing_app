import numpy as np
from scipy.stats import norm

from methods.close_form import european_option_bs_cf
from utils.constants import ONE_DAY
from utils.flag_utils import cp2omega


class BSGreeks:

    def __init__(self, option_type, S, K, T, r, q, sigma):
        self.option_type = option_type
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.q = q
        self.sigma = sigma

        # derived quantities
        self.omega = cp2omega(option_type)
        self.disc_r = np.exp(-r * T)
        self.disc_q = np.exp(-q * T)
        self.v = sigma * np.sqrt(T)
        self.d1 = (np.log(S / K) + ((r - q) * T + 0.5 * self.v**2)) / self.v
        self.d2 = self.d1 - self.v
        self.pd1 = norm.pdf(self.d1)
        self.nd1 = norm.cdf(self.omega * self.d1)
        self.nd2 = norm.cdf(self.omega * self.d2)

        self.price = european_option_bs_cf(option_type, S, K, T, r, q, sigma)

    @property
    def delta(self):
        return self.omega * self.disc_q * self.nd1

    @property
    def gamma(self):
        return self.pd1 * self.disc_q / (self.S * self.v)

    @property
    def vega(self):
        return self.S * self.pd1 * self.disc_q * np.sqrt(self.T) / 100

    @property
    def rho(self):
        if self.r - self.q == 0:
            return -self.T * self.price
        else:
            return self.omega * self.K * self.T * self.disc_r * self.nd2 / 100

    @property
    def theta(self):
        g = - (self.S * self.disc_q * self.pd1 * self.sigma) / (2 * np.sqrt(self.T)) \
            - self.omega * (-self.q * self.S * self.disc_q * self.nd1 + self.r * self.K * self.disc_r * self.nd2)
        return g * ONE_DAY

    @property
    def vanna(self):
        return - self.disc_q * self.d2 / self.sigma * self.pd1 / 100

    @property
    def volga(self):
        return self.vega * (self.d1 * self.d2) / (100 * self.sigma)


class HestonGreeks:
    def __init__(self, option_type, S, K, T, r, q, sigma):
        pass
