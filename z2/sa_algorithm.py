import math
import random
from functions import load_function_config


def make_acceptation_critter(fx: float,
                             fx_new: float,
                             temperature: float,
                             k: float) -> float:
    delta = fx_new - fx
    if delta >= 0:
        return 1
    else:
        return math.exp(delta / (k * temperature))


def sa_algorithm(function_id: int,
                 epochs: int,
                 temperature: float,
                 cooling_factor: float,
                 number_of_attempts: int,
                 k: float) -> tuple[float, float, list[float]]:
    config = load_function_config(function_id)
    function = config["func"]
    min_x, max_x = config["range"]

    x = random.uniform(min_x, max_x)
    temp = temperature

    solutions = [function(x)]

    for epoch in range(epochs):
        for attempt in range(number_of_attempts):
            fx = function(x)
            x_1 = max(x - (2 * temp), min_x)
            x_2 = min(x + (2 * temp), max_x)

            x_new = random.uniform(x_1, x_2)

            fx_new = function(x_new)

            acceptation_critter = make_acceptation_critter(fx, fx_new,
                                                           temp, k)

            if (acceptation_critter == 1 or
                    acceptation_critter > random.uniform(0, 1)):
                x = x_new
                solutions.append(fx_new)

        temp *= cooling_factor
    return x, function(x), solutions
