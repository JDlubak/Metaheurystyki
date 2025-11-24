import random


def single_point_crossing(parent1, parent2):
    crossing_point = random.randint(1, 25)
    print(f'Wylosowano: {crossing_point}')
    first_part = parent1['Name'][:crossing_point]
    second_part = parent2['Name'][crossing_point:]
    result = first_part + second_part
    return result


def double_point_crossing(parent1, parent2):
    first_point, second_point = sorted(random.sample(range(1, 26), 2))
    print(f'Wylosowano: {first_point} {second_point}')
    first_part = parent1['Name'][:first_point]
    middle_part = parent2['Name'][first_point:second_point]
    last_part = parent1['Name'][second_point:]
    result = first_part + middle_part + last_part
    return result


def mutate_individual(individual: dict, mutation_rate: float) -> None:
    if random.uniform(0, 1) < mutation_rate:
        mutation_index = random.randint(0, 25)
        print(f'Wylosowano: {mutation_index}')
        name = list(individual['Name'])
        name[mutation_index] = '0' if name[ mutation_index] == '1' else '1'
        individual['Name'] = ''.join(name)
