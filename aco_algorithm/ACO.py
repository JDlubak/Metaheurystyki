import random
import time
import numpy as np
from ant import Ant
from file import save_run
from plot import draw_route


def create_distance_matrix(data):
    coords = data[["x", "y"]].to_numpy()
    diff = coords[:, None, :] - coords[None, :, :]
    distance_matrix = np.sqrt((diff ** 2).sum(axis=2))
    return distance_matrix


def create_colony(size, n, p_random, alpha, beta):
    colony = []
    for _ in range(size):
        ant = Ant(n, p_random, alpha, beta)
        colony.append(ant)
    return colony


def run_iteration(colony, distance_matrix, pheromone_matrix, rho):
    for ant in colony:
        ant.create_path(distance_matrix, pheromone_matrix)
    pheromone_matrix *= (1 - rho)
    for ant in colony:
        distance = ant.distance
        for i in range(len(ant.path) - 1):
            a = ant.path[i]
            b = ant.path[i + 1]
            pheromone_matrix[a, b] += 100 / distance
            pheromone_matrix[b, a] += 100 / distance


def run_algorithm(file, distance_matrix, df, p_random, alpha, beta,
                  iterations, rho, col_size, plot=None):
    best = []
    worst = []
    avg = []
    n = len(df)
    pheromone_matrix = np.ones((n, n), dtype=float)
    colony = create_colony(col_size, n, p_random, alpha, beta)
    start_time = time.time()
    shortest = float("inf")
    best_path = random.choice(colony)
    for i in range(iterations):
        all_distances = []
        run_iteration(colony, distance_matrix, pheromone_matrix, rho)
        for ant in colony:
            all_distances.append(ant.distance)
            if ant.distance < shortest:
                best_path = ant.path.copy()
                shortest = ant.distance
        best.append(float(min(all_distances)))
        worst.append(float(max(all_distances)))
        avg.append(float(sum(all_distances) / len(all_distances)))
    end_time = time.time()
    time_elapsed = end_time - start_time
    if plot:
        draw_route(df, best_path, shortest)
    else:
        count = file[3:5]
        file_name = (f'results-{count}-{p_random}-{alpha}-{beta}-'
                           f'{iterations}-{rho}-{col_size}')
        save_run(best, worst, avg, time_elapsed,
                 best_path, shortest, file_name)
