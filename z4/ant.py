import random
from maths import get_probabilities


class Ant:
    def __init__(self, attraction_count, p_random, alpha, beta):
        self.count = attraction_count
        self.path = []
        self.unvisited = set(range(1, attraction_count + 1))
        self.p_random = p_random
        self.alpha = alpha
        self.beta = beta
        self.distance = None
        self.shortest = None
        self.best_path = None

    def calculate_distance(self, dm):
        total_distance = 0
        prev_attraction = self.path[0]
        for attraction in self.path[1:]:
            total_distance += dm.at[prev_attraction, attraction]
            prev_attraction = attraction
        self.distance = total_distance
        if self.shortest is None or self.distance < self.shortest:
            self.best_path = self.path.copy()
            self.shortest = total_distance

    def create_path(self, dm, pm):
        start = random.randint(1, self.count)
        self.path = [start]
        self.unvisited = set(range(1, self.count + 1)) - {start}
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
                for p in probabilities:
                    cumulative_probability += p['prob']
                    if r <= cumulative_probability:
                        next_attraction = p['next_goal']
                        break
            if next_attraction is None:
                print('something is no yes')
            else:
                self.unvisited.remove(next_attraction)
                self.path.append(next_attraction)



