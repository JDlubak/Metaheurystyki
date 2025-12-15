import random
import numpy as np


class Ant:
    def __init__(self, attraction_count, p_random, alpha, beta):
        self.count = attraction_count
        self.path = []
        self.p_random = p_random
        self.alpha = alpha
        self.beta = beta
        self.distance = 0

    def create_path(self, dm, pm):
        start = random.randint(0, self.count - 1)
        self.path = [start]
        unvisited = set(range(self.count)) - {start}
        self.distance = 0
        while unvisited:
            next_attraction = None
            if random.uniform(0, 1) < self.p_random:
                next_attraction = random.choice(list(unvisited))
            else:
                probabilities = self.get_probabilities(pm, dm,
                                                       self.path[-1],
                                                       unvisited)
                r = random.uniform(0, 1)
                cumulative_probability = 0
                for next_goal, prob in probabilities:
                    cumulative_probability += prob
                    if r <= cumulative_probability:
                        next_attraction = int(next_goal)
                        break
            self.distance += dm[self.path[-1], next_attraction]
            self.path.append(next_attraction)
            unvisited.remove(next_attraction)
        self.distance += dm[self.path[-1], start]
        self.path.append(start)

    def get_probabilities(self, pm, dm, loc, unvisited):
        epsilon = 1e-10
        u = np.array(list(unvisited))
        values = ((pm[loc, u] ** self.alpha) *
                  ((1 / (dm[loc, u] + epsilon)) ** self.beta))
        probs = values / values.sum()
        return list(zip(u, probs))
