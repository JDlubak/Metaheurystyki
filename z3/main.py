import time

from handle_population import create_population, cross_population, mutate_population
from selection import selection_algorithm
from load_save_operations import load_data, load_config, save_iteration_data, data_to_csv

item_list = load_data()
(crossing_probability, mutation_probability, population_size,
 iterations, crossing_method, selection_method) = load_config()

start_time = time.time()

population = create_population(item_list, population_size)
best, worst, worst_with_zero, avg = [], [], [], []
save_iteration_data(population, best, worst, worst_with_zero, avg)

for _ in range(iterations):
    selection = selection_algorithm(population, selection_method)
    next_generation = cross_population(selection, crossing_method, crossing_probability, item_list)
    mutate_population(next_generation, mutation_probability, item_list)
    population = next_generation
    save_iteration_data(population, best, worst, worst_with_zero, avg)

end_time = time.time()
total_time = end_time - start_time

data_to_csv(best, worst, worst_with_zero, avg, total_time)
