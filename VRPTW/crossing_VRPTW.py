import random
from typing import List


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


def pm_crossover(p1: List[int], p2: List[int], start: int, end: int) \
        -> tuple[List[int], List[int]]:
    # First step
    child = [None] * len(p1)
    child[start:end] = p1[start:end]
    # Second step
    for i in range(start, end):
        if p2[i] not in child:
            curr_val = p2[i]
            curr_pos = i
            while start <= curr_pos < end:
                val_to_find = p1[curr_pos]
                curr_pos = p2.index(val_to_find)
            child[curr_pos] = curr_val
    # Third step
    for i in range(len(p1)):
        if child[i] is None:
            child[i] = p2[i]
    return child


def single_point_crossing(p1: List[int], p2: List[int]) \
        -> tuple[List[int], List[int]]:
    point = random.randint(1, len(p1) - 1)
    first_child = pm_crossover(p1, p2, 0, point)
    second_child = pm_crossover(p2, p1, 0, point)
    return first_child, second_child


def double_point_crossing(p1: List[int], p2: List[int]) \
        -> tuple[List[int], List[int]]:
    point1, point2 = sorted(random.sample(range(1, len(p1)), 2))
    first_child = pm_crossover(p1, p2, point1, point2)
    second_child = pm_crossover(p2, p1, point1, point2)
    return first_child, second_child


def cross_algorithm(parent1: List[int], parent2: List[int],
                    method: str) -> tuple[List[int], List[int]]:
    if method not in ('single', 'double'):
        raise ValueError(f'Incorrect crossing method: {method}!')
    if len(parent1) != len(parent2):
        raise ValueError(f'Parents have different length!')
    if method == 'single':
        return single_point_crossing(parent1, parent2)
    elif method == 'double':
        return double_point_crossing(parent1, parent2)
    raise ValueError("Unexpected error has occurred in cross_algorithm")


p1 = list(range(15))
random.shuffle(p1)
p2 = list(range(15))
print(f'Parent1 {p1}\nParent2 {p2}')
print(cross_algorithm(p1, p2, method='double'))
