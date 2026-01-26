import math
import random
import statistics
import time

from crossing_VRPTW import cross_algorithm
from file import save_run
from individual import Individual
from mutation_VRPTW import relocate_mutation
from selection_VRPTW import selection_algorithm


class GeneticAlgorithm:
    def __init__(self, population_size: int, number_of_clients: int,
                 crossing_method: str, data: dict, iterations: int,
                 crossing_probability: float, selection_method: str,
                 mutation_probability: float, instance_name: str):
        self.population_size = population_size
        self.number_of_clients = number_of_clients
        self.population = []
        self.crossing_method = crossing_method
        self.selection_method = selection_method
        self.crossing_probability = crossing_probability
        self.mutation_probability = mutation_probability
        self.data = data
        self.iterations = iterations
        self.instance_name = instance_name

    def create_population(self):
        for _ in range(self.population_size):
            individual = Individual(self.number_of_clients)
            self.population.append(individual)

    def cross_population(self, selection: list[Individual]):
        new_population = []
        random.shuffle(selection)
        j = (math.ceil(self.crossing_probability * len(selection) / 2)
             * 2)
        for i in range(0, len(selection) - 1, 2):
            parent1 = selection[i]
            parent2 = selection[i + 1]
            if i < j:
                child1, child2 = cross_algorithm(parent1, parent2,
                                                 self.crossing_method)
                new_population.append(child1)
                new_population.append(child2)
            else:
                child1 = Individual(self.number_of_clients,
                                    list(parent1.order))
                child1.vehicles = list(parent1.vehicles)
                child1.value = parent1.value
                child1.evaluated = True
                child2 = Individual(self.number_of_clients,
                                    list(parent2.order))
                child2.vehicles = list(parent2.vehicles)
                child2.value = parent2.value
                child2.evaluated = True
                new_population.append(child1)
                new_population.append(child2)
        if len(selection) % 2 == 1:
            last = Individual(self.number_of_clients,
                              list(selection[-1].order))
            last.vehicles = list(selection[-1].vehicles)
            last.value = selection[-1].value
            last.evaluated = True
            new_population.append(last)
        self.population = new_population

    def mutate_population(self):
        mutated_count = math.ceil(self.mutation_probability * len(
            self.population))
        indexes = random.sample(range(len(self.population)),
                                mutated_count)
        for idx in indexes:
            relocate_mutation(self.population[idx])

    def run_iteration(self):
        best_ind = min(self.population, key=lambda x: x.value)
        previous_best_order = list(best_ind.order)
        previous_best_value = best_ind.value
        selection = selection_algorithm(self.population,
                                        self.selection_method)
        self.cross_population(selection)
        self.mutate_population()
        for individual in self.population:
            if individual.evaluated:
                continue
            individual.create_vehicles(self.data)
            individual.evaluate(self.data)
        worst_idx = self.population.index(max(self.population,
                                              key=lambda ind:
                                              ind.value))
        previous_best = Individual(self.number_of_clients,
                                   previous_best_order)
        previous_best.value = previous_best_value
        self.population[worst_idx] = previous_best

    def run(self, print_result: bool = True, task_id: int = None) -> (
            dict):
        best = []
        best_count = []
        worst = []
        worst_count = []
        avg = []
        avg_count = []
        std_dev = []
        std_dev_count = []
        start_time = time.time()
        self.create_population()
        for individual in self.population:
            individual.create_vehicles(self.data)
            individual.evaluate(self.data)
        overall_best = {
            'value': float('inf'),
            'order': [],
            'vehicles': []
        }

        for i in range(self.iterations):
            self.run_iteration()
            current_best = min(self.population,
                               key=lambda ind: ind.value)
            if current_best.value < overall_best['value']:
                overall_best['value'] = current_best.value
                overall_best['order'] = list(current_best.order)
                overall_best['vehicles'] = list(current_best.vehicles)
            if (i + 1) % 10 == 0 and print_result:
                best_val = overall_best['value']
                distance = best_val % 10000
                vehicles = best_val // 10000
                print(
                    f'Iteracja {i + 1}/{self.iterations}: '
                    f'Liczba pojazdów: {vehicles:.0f} '
                    f'Dystans: {distance:.3f}')
            values = [ind.value for ind in self.population]
            distances = [val % 10000 for val in values]
            counts = [int(val // 10000) for val in values]
            best.append(overall_best['value'] % 10000)
            best_count.append(overall_best['value'] // 10000)
            worst.append(max(distances))
            worst_count.append(max(counts))
            avg.append(sum(distances) / len(distances))
            avg_count.append(sum(counts) / len(counts))
            std_dev.append(statistics.stdev(distances))
            std_dev_count.append(statistics.stdev(counts))

        elapsed_time = time.time() - start_time
        data = [best, best_count, worst, worst_count,
                avg, avg_count, std_dev, std_dev_count]
        parameters = [self.population_size, self.iterations,
                      self.crossing_probability, self.crossing_method,
                      self.mutation_probability, self.selection_method]
        save_run(self.instance_name, data, parameters, elapsed_time,
                 overall_best['vehicles'], task_id)
        return overall_best, elapsed_time
