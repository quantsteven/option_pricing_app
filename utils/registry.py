from typing import Union

from greeks.analytical import BSGreeks, HestonGreeks
from greeks.numerical import FDGreeks
from methods import close_form

# ------------ 0. 支付函数注册 -----------------
PAYOFFS = {
    "European Option": close_form.european_option_payoff,
    "Single Touch Option": close_form.single_touch_option_payoff,
    "Double Touch Option": close_form.double_touch_option_payoff,
    "Single Barrier Option": close_form.single_barrier_option_payoff,
    "Double Barrier Option": close_form.double_barrier_option_payoff,
}

# ------------ 1. 定价函数注册 -----------------
PRICERS = {
    "Black-Scholes": {
        "European Option": {
            "Close-Form": close_form.european_option_bs_cf,
            "PDE Finite Difference": None,
            "Monte Carlo": None,
        },
        "Single Touch Option": {
            "Close-Form": close_form.single_touch_option_bs_cf,
            "PDE Finite Difference": None,
            "Monte Carlo": None,
        },
        "Double Touch Option": {
            "Close-Form": close_form.double_touch_option_bs_cf,
            "PDE Finite Difference": None,
            "Monte Carlo": None,
        },
        "Single Barrier Option": {
            "Close-Form": close_form.single_barrier_option_bs_cf,
            "PDE Finite Difference": None,
            "Monte Carlo": None,
        },
        "Double Barrier Option": {
            "Close-Form": close_form.double_barrier_option_bs_cf,
            "PDE Finite Difference": None,
            "Monte Carlo": None,
        },
    },
    "Heston": {
        "European Option": {
            "Close-Form": close_form.european_option_heston_cf,
            "PDE Finite Difference": None,
            "Monte Carlo": None,
        },
        "Single Touch Option": {
            "Close-Form": None,
            "PDE Finite Difference": None,
            "Monte Carlo": None,
        },
        "Double Touch Option": {
            "Close-Form": None,
            "PDE Finite Difference": None,
            "Monte Carlo": None,
        },
        "Single Barrier Option": {
            "Close-Form": None,
            "PDE Finite Difference": None,
            "Monte Carlo": None,
        },
        "Double Barrier Option": {
            "Close-Form": None,
            "PDE Finite Difference": None,
            "Monte Carlo": None,
        },
    }
}

# ------------ 2. Greeks 引擎注册 -------------
num_greeks_factory = lambda function, parameter: FDGreeks(function, parameter)
GREEK_ENGINES = {
    "Black-Scholes": {
        "European Option": {
            "analytical": lambda parameter: BSGreeks(**parameter),
            "numerical": num_greeks_factory,
        },
        "Single Touch Option": {"numerical": num_greeks_factory},
        "Double Touch Option": {"numerical": num_greeks_factory},
        "Single Barrier Option": {"numerical": num_greeks_factory},
        "Double Barrier Option": {"numerical": num_greeks_factory},
    },
    "Heston": {
        "European Option": {
            "analytical": lambda parameter: HestonGreeks(**parameter),
            "numerical": num_greeks_factory,
        },
        "Single Touch Option": {"numerical": num_greeks_factory},
        "Double Touch Option": {"numerical": num_greeks_factory},
        "Single Barrier Option": {"numerical": num_greeks_factory},
        "Double Barrier Option": {"numerical": num_greeks_factory},
    },
}


# ------------ 3. 公共工具函数 ----------------
def get_payoff(instrument: str, param: dict) -> Union[None, float]:
    payoff = PAYOFFS.get(instrument)
    return None if payoff is None else payoff(**param)


def get_price(model: str, instrument: str, method: str, param: dict) -> Union[None, float]:
    pricer = PRICERS.get(model).get(instrument).get(method)
    return None if pricer is None else pricer(**param)


def get_greeks(model: str, instrument: str, method: str, param: dict, selected: list[str]) -> Union[None, dict]:
    func = PRICERS.get(model).get(instrument).get(method)
    engine = GREEK_ENGINES.get(model).get(instrument)
    if not func or not engine or not selected:
        return None
    out = {}
    for label, factory in engine.items():
        engine = factory(param) if label.lower() == "analytical" else factory(func, param)
        out[label.capitalize()] = {g: getattr(engine, g.lower()) for g in selected}
    return out
