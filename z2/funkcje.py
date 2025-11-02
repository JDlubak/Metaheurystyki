import math
import random

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

def smith_simulator(func_id: int, M: int, T0: float, k: float):
    if func_id not in FUNCTIONS:
        raise ValueError("Niepoprawny wybór funkcji (1 lub 2).")

    cfg = FUNCTIONS[func_id]
    f = cfg["func"]
    min_x, max_x = cfg["range"]

    x = random.uniform(min_x, max_x)
    fx = f(x)
    x_best = x
    fx_best = fx

    for i in range(M):
        x_new = x + random.uniform(min_x/10, max_x/10)
        x_new = max(min_x, min(max_x, x_new))
        fx_new = f(x_new)

        delta = fx_new - fx
        if delta > 0 or random.uniform(0,1) < math.exp(delta/T0):
            x = x_new
            fx = fx_new
            if fx > fx_best:
                fx_best = fx
                x_best = x
        T0 *= k
    return x_best, fx_best
