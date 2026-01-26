import random

from individual import Individual


def set_adaptation_in_population(population: list[Individual],
                                 selection_type: str):
    if selection_type == 'ranking':
        population = sorted(population, key=lambda x: x.value)
        n = len(population)
        for rank, ind in enumerate(population, start=1):
            ind.adaptation = (n - rank + 1) / (n * (n + 1) / 2)
    else:
        raise ValueError(f'Incorrect selection_type: {selection_type}!')


def selection_algorithm(population: list[Individual],
                        selection_type: str) -> list[Individual]:
    population_size = len(population)
    if population_size == 0:
        raise ValueError('Please create population!')
    selected = []
    if selection_type == 'tournament':
        for _ in range(population_size):
            tournament = random.sample(population, 5)
            winner = min(tournament, key=lambda x: x.value)
            selected.append(winner)
    elif selection_type == 'ranking':
        set_adaptation_in_population(population, selection_type)
        adaptation_sum = 0
        cumulative_adaptation = []
        for individual in population:
            adaptation_sum += individual.adaptation
            cumulative_adaptation.append(adaptation_sum)
        cumulative_adaptation[-1] = 1.0
        for _ in range(population_size):
            r = random.random()
            for index, limit in enumerate(cumulative_adaptation):
                if r <= limit:
                    selected.append(population[index])
                    break
    return selected
