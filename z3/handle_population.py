import random


def create_population(items, size):
    population = []
    for _ in range(size):
        individual = create_individual()
        value = calculate_value(items, individual)
        population.append(
            {'Value': value, 'Generation': 0, 'Name': individual})
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
