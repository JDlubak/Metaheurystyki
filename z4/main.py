import pandas as pd

from ant import create_colony
from maths import create_distance_matrix
from file import read_file


df = read_file('A-n32-k5.txt')
distance_matrix = create_distance_matrix(df)
pheromone_matrix = pd.DataFrame(1, index=df.index, columns=df.index)
# pheromone_matrix.values *= (1 - rho) - do aktualizacji

colony = create_colony(1, len(df), 0.1, 2, 3)
for ant in colony:
    ant.create_path(distance_matrix, pheromone_matrix)
    print(ant.path)
