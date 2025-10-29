import math

# Funkcja z rozdziału 3
def far_extremum_function(x: float) -> float:
    if -105 < x < -95:
        return -2 * abs(x + 100) + 10
    elif 95 < x < 105:
        return -2.2 * abs(x - 100) + 11
    else:
        return 0

# Funkcja z rozdziału 4
def close_extremum_function(x: float) -> float:
    return x * math.sin(10 * math.pi * x) + 1

