import math


def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    value = math.floor(n * multiplier) / multiplier

    return value if value >= 0 else 0.0
