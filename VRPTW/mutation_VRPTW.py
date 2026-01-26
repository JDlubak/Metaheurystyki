import random

from individual import Individual


def relocate_mutation(ind: Individual):
    if len(ind.order) < 2:
        return
    idx = random.randrange(len(ind.order))
    customer = ind.order.pop(idx)
    new_idx = random.randrange(len(ind.order) + 1)
    ind.order.insert(new_idx, customer)
