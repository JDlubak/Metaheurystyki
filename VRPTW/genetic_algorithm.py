import math
import random

from individual import Individual
from crossing_VRPTW import cross_algorithm
from VRPTW.mutation_VRPTW import mutation_algorithm


class GeneticAlgorithm:
    def __init__(self, population_size: int, number_of_clients: int,
                 crossing_method: str, mutation_method: str,
                 data: dict, crossing_probability: float,
                 mutation_probability: float, selection_method: str):
        self.population_size = population_size
        self.number_of_clients = number_of_clients
        self.population = []
        self.crossing_method = crossing_method
        self.mutation_method = mutation_method
        self.selection_method = selection_method
        self.crossing_probability = crossing_probability
        self.mutation_probability = mutation_probability
        self.data = data

    def create_population(self):
        for _ in range(self.population_size):
            individual = Individual(self.number_of_clients)
            self.population.append(individual)

    def sort_population(self):
        self.population = sorted(self.population,
                                 key=lambda individual:
                                 individual.value)

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
                new_population.append(parent1.copy())
                new_population.append(parent2.copy())
            if len(selection) % 2 == 1:
                new_population.append(selection[-1].copy())

    def mutate_population(self):
        random.shuffle(self.population)
        mutated_count = math.ceil(self.mutation_probability * len(
            self.population))
        for i in range(0, mutated_count):
            mutation_algorithm(self.population[i], self.mutation_method)

    def run_iteration(self):
        for individual in self.population:
            individual.create_vehicles()
            individual.evaluate()
        self.sort_population()


ga = GeneticAlgorithm(population_size=100, number_of_clients=10)
ga.create_population()
print(ga.population)


