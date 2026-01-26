from genetic_algorithm import GeneticAlgorithm
from file import read_solomon_data, load_config

data = read_solomon_data('solomon-100/In/c101.txt')

number_of_clients = len(data['customers']) - 1
cp, mp, p, i, cm, sm = load_config()

ga = GeneticAlgorithm(population_size=p,
                      crossing_method=cm,
                      selection_method=sm,
                      mutation_probability=mp,
                      crossing_probability=cp,
                      iterations=i,
                      number_of_clients=number_of_clients,
                      data=data)

best = ga.run()

print('---------------------------------')
for vehicle in best['vehicles']:
    print(vehicle.route)
