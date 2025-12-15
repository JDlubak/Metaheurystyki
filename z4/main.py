import random

from ACO import create_colony, run_iteration
from maths import create_matrices
from file import read_file
from plot import draw_route

df = read_file('A-n32-k5.txt')
distance_matrix, pheromone_matrix = create_matrices(df)
p_random = 0.01
alpha = 20
beta = 10
iterations = 10
rho = 0.5

colony = create_colony(600, len(df), p_random, alpha, beta)
best_ant = random.choice(colony)
for i in range(iterations):
    print(f'Iteration: {i + 1}')
    run_iteration(colony, distance_matrix, pheromone_matrix, rho)
    for ant in colony:
        if ant.shortest < best_ant.shortest:
            best_ant = ant
            
draw_route(df, best_ant.best_path)
