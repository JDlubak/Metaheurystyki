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

def delta(func1, func2):
    return func2 - func1

def make_acceptation_critter(func1, func2, temperature):
    if delta(func1, func2) >= 0:
        return 1
    elif delta(func1, func2) < 0:
        return math.exp(delta(func1, func2) / temperature)

def load_function_config(func_id):
    if func_id not in FUNCTIONS:
        raise ValueError("Niepoprawny wybór funkcji (1 lub 2).")
    config = FUNCTIONS[func_id]
    return config

def sa_algorithm(function_id: int, epochs: int, temperature: float, cooling_factor: float, number_of_attempts: int):
    config = load_function_config(function_id)
    function = config["func"]
    min_x, max_x = config["range"]

    x = random.uniform(min_x, max_x)
    fx = function(x)
    temp = temperature

    for epoch in range(epochs):
        for attempt in range(number_of_attempts):
            x_1 = max(x - (2 * temp), min_x)
            x_2 = min(x + (2 * temp), max_x)

            x_new = random.uniform(x_1, x_2)
            fx_new = function(x_new)

            acceptation_critter = make_acceptation_critter(fx, fx_new, temp)

            if acceptation_critter > random.uniform(0,1):
                x = x_new

        temp *= cooling_factor
    return x, function(x)
