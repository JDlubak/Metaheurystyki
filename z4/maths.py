import numpy as np


def create_matrices(data):
    coords = data[["x", "y"]].to_numpy()
    diff = coords[:, None, :] - coords[None, :, :]
    distance_matrix = np.sqrt((diff ** 2).sum(axis=2))
    n = len(data)
    pheromone_matrix = np.ones((n, n), dtype=float)
    return distance_matrix, pheromone_matrix


def get_probabilities(pm, dm, loc, unvisited, alpha, beta):
    epsilon = 1e-10
    u = np.array(list(unvisited))
    values = ((pm[loc, u] ** alpha) *
              ((1 / (dm[loc, u] + epsilon)) ** beta))
    probs = values / values.sum()
    return list(zip(u, probs))
