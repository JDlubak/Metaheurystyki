import random
from typing import List


def swap_mutation(ind: List[int]) -> List[int]:
    idx1, idx2 = random.sample(range(len(ind)), 2)
    ind[idx1], ind[idx2] = ind[idx2], ind[idx2]
    return ind


def inversion_mutation(ind: List[int]) -> List[int]:
    idx1, idx2 = random.sample(range(len(ind)), 2)
    ind[idx1:idx2] = ind[idx1:idx2][::-1]
    return ind


def mutation_algorithm(individual: List[int], method: str) -> List[int]:
    if method not in ('swap', 'inversion'):
        raise ValueError(f'Incorrect mutation method: {method}!')
    if method == 'swap':
        return swap_mutation(individual)
    elif method == 'inversion':
        return inversion_mutation(individual)
    raise ValueError("Unexpected error has occurred "
                     "in mutation_algorithm")
