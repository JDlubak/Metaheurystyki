import random
import pandas as pd

from ACO import create_colony, run_iteration
from maths import create_distance_matrix
from file import read_file


df = read_file('A-n32-k5.txt')
distance_matrix = create_distance_matrix(df)
pheromone_matrix = pd.DataFrame(1, index=df.index, columns=df.index,
                                dtype=float)
p_random = 0.1
alpha = 2
beta = 3
iterations = 300
rho = 0.1

colony = create_colony(30, len(df), p_random, alpha, beta)
best_ant = random.choice(colony)
for i in range(iterations):
    print(f'Iteration: {i}')
    run_iteration(colony, distance_matrix, pheromone_matrix, rho)
    for ant in colony:
        if ant.distance < best_ant.distance:
            best_ant = ant
for ant in colony:
    print(ant.shortest)
    print(ant.best_path)
