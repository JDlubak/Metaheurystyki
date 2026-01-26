import random

from VRPTW.individual import Individual


def swap_mutation(ind: Individual):
    idx1, idx2 = random.sample(range(len(ind.order)), 2)
    ind.order[idx1], ind.order[idx2] = ind.order[idx2], ind.order[idx1]


def inversion_mutation(ind: Individual):
    idx1, idx2 = sorted(random.sample(range(len(ind.order)), 2))
    ind.order[idx1:idx2] = ind.order[idx1:idx2][::-1]


def mutation_algorithm(individual: Individual, method: str):
    if method not in ('swap', 'inversion'):
        raise ValueError(f'Incorrect mutation method: {method}!')
    if method == 'swap':
        swap_mutation(individual)
    elif method == 'inversion':
        inversion_mutation(individual)
    raise ValueError("Unexpected error has occurred "
                     "in mutation_algorithm")
