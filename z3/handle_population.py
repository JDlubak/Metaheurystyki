import random
import math
from crossing import cross_algorithm


def create_population(items: dict, size: int) -> list[dict]:
    population = []
    for _ in range(size):
        individual = create_individual()
        value = calculate_value(items, individual)
        population.append(
            {'Name': individual, 'Value': value})
    return population


def create_individual() -> str:
    selected = random.randint(0, 67_108_863)
    return format(selected, '026b')
    # Napis typu 10100101101111011110101000 - liczba 26-bitowa.
    # Interpretacja -> wkładamy do plecaka 1 element, 3, 6, 8, 9 itd.


def calculate_value(items: dict, individual: dict) -> int:
    BACKPACK_LIMIT = 6_406_180
    total_weight = 0
    total_value = 0
    for i in range(0, 26):
        if individual[i] == '1':
            total_weight += items[i + 1]['Weight']
            total_value += items[i + 1]['Value']
            if total_weight > BACKPACK_LIMIT:
                return 0
    return total_value


def cross_population(selection: list[dict], crossing_method: str,
                     crossing_probability: float, items: dict) -> list[dict]:
    new_population = []
    random.shuffle(selection)
    j = math.ceil(crossing_probability * len(selection) / 2) * 2
    for i in range(0, len(selection) - 1, 2):
        parent1 = selection[i]
        parent2 = selection[i + 1]
        if i < j:
            child1_name, child2_name = cross_algorithm(parent1['Name'],
                                                       parent2['Name'], crossing_method)
            new_population.append({'Name': child1_name,
                                   'Value': calculate_value(items, child1_name)})
            new_population.append({'Name': child2_name,
                                   'Value': calculate_value(items, child2_name)})
        else:
            new_population.append(parent1.copy())
            new_population.append(parent2.copy())
    if len(selection) % 2 == 1:
        new_population.append(selection[-1].copy())
    return new_population


def mutate_population(selection: list[dict], mutation_probability: float, items: dict) -> None:
    random.shuffle(selection)
    mutated_count = math.ceil(mutation_probability * len(selection))
    for i in range(0, mutated_count):
        name = list(selection[i]['Name'])
        mutation_index = random.randint(0, len(name) - 1)
        name[mutation_index] = '0' if name[mutation_index] == '1' else '1'
        selection[i]['Name'] = ''.join(name)
        selection[i]['Value'] = calculate_value(items, selection[i]['Name'])
