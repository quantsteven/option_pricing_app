from utils.constants import ONE_DAY

GREEK_CONFIG = {

    "delta": {'shock_mode': 'center', 'shock_type': 'relative', 'shock_magnitude': 1, 'shock_unit': '%'},
    "gamma": {'shock_mode': 'center', 'shock_type': 'relative', 'shock_magnitude': 1, 'shock_unit': '%'},
    "vega": {'shock_mode': 'up', 'shock_type': 'absolute', 'shock_magnitude': 1, 'shock_unit': '%'},
    "rho": {'shock_mode': 'up', 'shock_type': 'absolute', 'shock_magnitude': 1, 'shock_unit': 'bp'},
    "volga": {'shock_mode': 'center', 'shock_type': 'absolute', 'shock_magnitude': 1, 'shock_unit': '%'},
    "vanna": {'shock_mode': 'center', 'shock_type': 'absolute', 'shock_magnitude': 1, 'shock_unit': '%'},
    "theta": {'shock_mode': 'down', 'shock_type': 'absolute', 'shock_magnitude': ONE_DAY, 'shock_unit': ''}
}
