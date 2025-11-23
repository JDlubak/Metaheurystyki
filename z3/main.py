import pandas as pd
import random


def load_data() -> dict:
    data = pd.read_csv('problem plecakowy dane CSV tabulatory.csv',
                       sep='\t')
    data = data.rename(columns={'Nazwa': 'Name',
                                'Waga (kg)': 'Weight',
                                'Wartość (zł)': 'Value'})
    data['Weight'] = data['Weight'].str.replace(' ', '').astype(int)
    data['Value'] = data['Value'].str.replace(' ', '').astype(int)
    items = data.set_index('Numer').to_dict('index')
    return items


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


def create_population(items, size):
    population = []
    for _ in range(size):
        individual = create_individual()
        value = calculate_value(items, individual)
        population.append(
            {'Value': value, 'Generation': 0, 'Name': individual})
    return population


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
        name[mutation_index] = '0' if name[mutation_index] == '1' else '1'
        individual['Name'] = ''.join(name)


item_list = load_data()
population = create_population(item_list, 100)

# test sortowania
population.sort(key=lambda x: (-x['Value'], -x['Generation']))
for item in population:
    print(item)

# test krzyżowania
print(f'Pierwszy osobnik: {population[0]['Name']}\nDrugi osobnik: {population[1]['Name']}')

print(single_point_crossing(population[0], population[1]))
print(double_point_crossing(population[0], population[1]))

# test mutacji
print(f'Mutowany osobnik: {population[0]['Name']}')
mutate_individual(population[0], 4)
print(f'Po mutacji: {population[0]['Name']}')
