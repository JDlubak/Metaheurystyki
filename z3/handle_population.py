import random
from crossing import cross_algorithm

def create_population(items, size):
    population = []
    for _ in range(size):
        individual = create_individual()
        value = calculate_value(items, individual)
        population.append(
            {'Name': individual, 'Value': value})
    return population


def create_individual():
    selected = random.randint(0, 67_108_863)
    return format(selected, '026b')
    # Napis typu 10100101101111011110101000 - liczba 26-bitowa.
    # Interpretacja -> wkładamy do plecaka 1 element, 3, 6, 8, 9 itd.


def calculate_value(items, individual):
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
    for i in range(0, len(selection) - 1, 2):
        parent1 = selection[i]
        parent2 = selection[i + 1]
        child1_name, child2_name = cross_algorithm(parent1['Name'], parent2['Name'],
                                                   crossing_probability, crossing_method)
        new_population.append({'Name': child1_name, 'Value': calculate_value(items, child1_name)})
        new_population.append({'Name': child2_name, 'Value': calculate_value(items, child2_name)})
    if len(selection) % 2 == 1:
        new_population.append(selection[-1].copy())
    return new_population


def mutate_population(selection: list[dict], mutation_probability: float,
                      items: dict, mutated_bits: int) -> None:
    for item in selection:
        if random.uniform(0, 1) < mutation_probability:
            bits_to_change = random.sample(range(len(item['Name'])), mutated_bits)
            name = list(item['Name'])
            for bit in bits_to_change:
                name[bit] = '0' if name[bit] == '1' else '1'
            item['Name'] = ''.join(name)
            item['Value'] = calculate_value(items, item['Name'])
