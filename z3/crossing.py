import random


def single_point_crossing(parent1: str, parent2: str, n: int) -> tuple[str, str]:
    p = random.randint(1, n - 1)
    first_child = parent1[:p] + parent2[p:]
    second_child = parent2[:p] + parent1[p:]
    return first_child, second_child


def double_point_crossing(parent1: str, parent2: str, n: int) -> tuple[str, str]:
    p1, p2 = sorted(random.sample(range(1, n), 2))
    first_child = parent1[:p1] + parent2[p1:p2] + parent1[p2:]
    second_child = parent2[:p1] + parent1[p1:p2] + parent2[p2:]
    return first_child, second_child


def cross_algorithm(parent1: str, parent2: str,
                    crossing_probability: float, crossing_method: str) -> tuple[str, str]:
    if crossing_method not in ('single', 'double'):
        raise ValueError(f'Błędna metoda krzyżowania: {crossing_method}. Użyj "single"/"double"')
    n1, n2 = len(parent1), len(parent2)
    if n1 != n2:
        raise ValueError(f'Nieoczekiwany błąd: Rodzice mają różną długość! ({n1}, {n2})')
    if random.uniform(0, 1) > crossing_probability:
        return parent1, parent2
    elif crossing_method == 'single':
        return single_point_crossing(parent1, parent2, n1)
    elif crossing_method == 'double':
        return double_point_crossing(parent1, parent2, n1)
    raise ValueError("Nieoczekiwany błąd: cross_algorithm nic nie zwrócił!")
