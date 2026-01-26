import random

from individual import Individual


def relocate_mutation(ind: Individual, method: str):
    if len(ind.order) < 4:
        return
    if method == 'chunk':
        chunk_size = random.randint(2, 3)
    else:
        chunk_size = 1
    start_idx = random.randrange(len(ind.order) - chunk_size + 1)
    chunk = []
    for _ in range(chunk_size):
        chunk.append(ind.order.pop(start_idx))
    new_idx = random.randrange(len(ind.order) + 1)
    for (i, customer) in enumerate(chunk):
        ind.order.insert(new_idx + i, customer)
