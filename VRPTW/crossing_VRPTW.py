import random
from typing import List

from individual import Individual


# Crossover algorithm for VRPTW has to be adapted, we cannot use
# implementation directly from genetic_algorithm created before,
# because now a chromosome represents a sequence of unique clients.
#
# Let's say we have 2 different orders of clients to visit:
# P1: [1, 2, 3 | 4, 5, 6, 7]
# P2: [2, 1, 4 | 5, 3, 7, 6]
# Results: [1, 2, 3, 5, 3, 7, 6], [2, 1, 4, 4, 5, 6, 7]
# In the first child, 4 is missing, and 3 occurs twice, and in the
# second child, we get the opposite - 4 occurs twice, 3 is missing.
#
# As each client must be visited exactly once, we have to create a
# solution for this problem, which is Partially Mapped Crossover.
# It maintains a valid permutation in 3 steps:
# 1. Copying a selected segment from first parent.
# 2. Creating a mapping between the elements of segment in P1 and P2,
# and resolving potential conflicts using this mapping to make sure no
# # conflicts or omissions occur.
# 3. Filling remaining positions using Parent 2.


def pm_crossover(p1_order: List[int], p2_order: List[int],
                 start: int, end: int) -> List[int]:
    # First step
    size = len(p1_order)
    child_order = [None] * size
    child_order[start:end] = p1_order[start:end]

    p2_map = {val: idx for idx, val in enumerate(p2_order)}

    # Second step
    for i in range(start, end):
        if p2_order[i] not in child_order:
            curr_val = p2_order[i]
            curr_pos = i
            while start <= curr_pos < end:
                val_to_find = p1_order[curr_pos]
                curr_pos = p2_map[val_to_find]
            child_order[curr_pos] = curr_val
    # Third step
    for i in range(size):
        if child_order[i] is None:
            child_order[i] = p2_order[i]
    return child_order


def cross_algorithm(parent1: Individual, parent2: Individual,
                    cross_method: str) -> tuple[Individual, Individual]:
    if len(parent1.order) != len(parent2.order):
        raise ValueError(f'Parents have different length!')
    size = len(parent1.order)
    if cross_method == 'single':
        point = random.randint(1, size - 1)
        start, end = 0, point
    elif cross_method == 'double':
        start, end = sorted(random.sample(range(size), 2))
    else:
        raise ValueError(f'Incorrect crossing method: {cross_method}!')
    order_1 = pm_crossover(parent1.order, parent2.order, start, end)
    order_2 = pm_crossover(parent2.order, parent1.order, start, end)
    child1 = Individual(size, order_1)
    child2 = Individual(size, order_2)
    return child1, child2

