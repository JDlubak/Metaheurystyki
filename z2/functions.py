import math


# Funkcja z rozdziału 3 przedzial [-150,150]
def far_extremum_function(x: float) -> float:
    if -105 < x < -95:
        return -2 * abs(x + 100) + 10
    elif 95 < x < 105:
        return -2.2 * abs(x - 100) + 11
    else:
        return 0


# Funkcja z rozdziału 4 przedzial [-1,2]
def close_extremum_function(x: float) -> float:
    return x * math.sin(10 * math.pi * x) + 1


FUNCTIONS = {
    1: {
        "func": far_extremum_function,
        "range": (-150, 150)
    },
    2: {
        "func": close_extremum_function,
        "range": (-1, 2)
    }
}


def load_function_config(func_id: int) -> dict:
    if func_id not in FUNCTIONS:
        raise ValueError("Niepoprawny wybór funkcji (1 lub 2).")
    config = FUNCTIONS[func_id]
    return config
