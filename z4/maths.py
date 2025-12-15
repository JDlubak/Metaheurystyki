import math
import pandas as pd


def get_location(data, index):
    return data.loc[index, ['x', 'y']].values


def calculate_distance(data, index1, index2):
    x1, y1 = get_location(data, index1)
    x2, y2 = get_location(data, index2)
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def create_distance_matrix(data):
    distance_matrix = pd.DataFrame()
    for i in data.index:
        for j in data.index:
            distance_matrix.at[i, j] = calculate_distance(data, i, j)
    return distance_matrix


def get_probabilities(pm, dm, loc, unvisited, alpha, beta):
    probabilities = []
    denominator = sum(pm.at[loc, u] ** alpha
                      * (1/dm.at[loc, u]) ** beta
                      for u in unvisited)
    for next_goal in unvisited:
        prob = (pm.at[loc, next_goal] ** alpha
                * (1/dm.at[loc, next_goal]) ** beta / denominator)
        probabilities.append({'next_goal': next_goal, 'prob': prob})
    return probabilities

