import random
from maths import get_probabilities


class Ant:
    def __init__(self, attraction_count, p_random, alpha, beta):
        self.count = attraction_count
        self.path = []
        self.unvisited = set(range(self.count))
        self.p_random = p_random
        self.alpha = alpha
        self.beta = beta
        self.distance = None
        self.shortest = None
        self.best_path = None

    def create_path(self, dm, pm):
        start = random.randint(0, self.count - 1)
        self.path = [start]
        self.unvisited = set(range(self.count)) - {start}
        self.distance = 0
        while self.unvisited:
            next_attraction = None
            if random.uniform(0, 1) < self.p_random:
                next_attraction = random.choice(list(self.unvisited))
            else:
                probabilities = get_probabilities(pm, dm, self.path[-1],
                                                  self.unvisited,
                                                  self.alpha, self.beta)
                r = random.uniform(0, 1)
                cumulative_probability = 0
                for next_goal, prob in probabilities:
                    cumulative_probability += prob
                    if r <= cumulative_probability:
                        next_attraction = int(next_goal)
                        break
            self.distance += dm[self.path[-1], next_attraction]
            self.path.append(next_attraction)
            self.unvisited.remove(next_attraction)
        self.distance += dm[self.path[-1], start]
        self.path.append(start)
        if self.shortest is None or self.distance < self.shortest:
            self.best_path = self.path.copy()
            self.shortest = self.distance
