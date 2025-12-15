from ant import Ant


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
        start = ant.path[0]
        for next_goal in ant.path[1:]:
            pheromone_matrix[start, next_goal] += 1 / distance
            pheromone_matrix[next_goal, start] += 1 / distance
