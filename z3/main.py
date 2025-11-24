from handle_population import create_population
from selection import selection_algorithm
from load_operations import load_data, load_config


item_list = load_data()
(cross_probability, mutation_probability, population_size,
 iterations, crossing_method, selection_method) = load_config()

population = create_population(item_list, population_size)
selection = selection_algorithm(population, 20, 'roulette')
for item in selection:
    print(item)



