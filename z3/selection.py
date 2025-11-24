import random


def set_adaptation_in_population(selection_type: str, population: list[dict]) -> list[dict]:
    if selection_type == 'roulette':
        total_adaptation = sum(ind['Value'] for ind in population)
        for ind in population:
            ind['Adaptation'] = ind['Value'] / total_adaptation \
                if total_adaptation > 0 else 1 / len(population)
    elif selection_type == 'ranking':
        population = sorted(population, key=lambda x: x['Value'], reverse=True)
        n = len(population)
        for rank, ind in enumerate(population, start=1):
            ind['Adaptation'] = (n - rank + 1) / (n * (n + 1) / 2)
            # (n * (n + 1) / 2) - wzór na sumę liczb od 1 do n
            # (n - rank + 1) - dla 1 będzie n, dla 2 n-1... dla ostatniego 1 - zgodnie z prezką
            # po podzieleniu mamy adaptację
            # do opisania w sprawku i potem usuniemy ten komentarz
    else:
        raise ValueError(f'Błędny typ selekcji: {selection_type}. Użyj "roulette"/"ranking"')
    return population


def selection_algorithm(population: list[dict], amount_of_selected: int, selection_type: str) -> list[dict]:
    if len(population) == 0:
        raise ValueError('Proszę utworzyć populację!')
    if amount_of_selected > len(population):
        raise ValueError(f'Proszę wybrać mniej osobników w metodzie ruletki - wybrana liczba '
                         f'{amount_of_selected} przekracza rozmiar populacji {len(population)}!')
    population = set_adaptation_in_population(selection_type, population)
    selected = []
    adaptation_sum = 0
    cumulative_adaptation = []
    for individual in population:
        adaptation_sum += individual['Adaptation']
        cumulative_adaptation.append(adaptation_sum)
    for _ in range(amount_of_selected):
        r = random.uniform(0, 1)
        for index, limit in enumerate(cumulative_adaptation):
            if r <= limit:
                selected.append(population[index])
                break
    return selected
