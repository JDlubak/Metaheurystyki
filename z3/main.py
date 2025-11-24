from handle_population import create_population, cross_population, mutate_population
from selection import selection_algorithm
from load_operations import load_data, load_config


item_list = load_data()
(crossing_probability, mutation_probability, population_size,
 iterations, crossing_method, selection_method, mutated_bits) = load_config()

population = create_population(item_list, population_size)
print("Startowa populacja: ")
for item in population:
    print(item)
for _ in range(iterations):
    selection = selection_algorithm(population, selection_method)
    next_generation = cross_population(selection, crossing_method, crossing_probability, item_list)
    mutate_population(next_generation, mutation_probability, item_list, mutated_bits)
    population = next_generation
    print("ITERACJA " + str(_))
    for item in population:
        print(item)
for item in population:
    print(item)


