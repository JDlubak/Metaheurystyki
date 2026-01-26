import json

import numpy as np


def read_solomon_data(file_path: str) -> dict:
    """
    :param file_path: Path to the Solomon VRPTW data file.
    :return: A dictionary containing all relevant data.

    How to access the data? Example:
    result = read_solomon_data(file_path)
    result['instance_name'], result['vehicle_max_count'],
    result['vehicle_capacity'], result['customers']
    result['distance_matrix'].
    If you want to access specific customer data:
    home = result['customers'][0] - customer with ID 0 is a home depot
    demand_1 = result['customers'][1]['demand'] - for accessing a field
    """
    with open(file_path, 'r') as f:
        lines = [line.split() for line in f if line.strip()]
    instance_name = lines[0][0]
    vehicle_max_count, vehicle_capacity = map(int, lines[3])
    customer_data_start_idx = 0
    for i, line in enumerate(lines):
        if line and line[0] == '0':
            customer_data_start_idx = i
            break
    customers = {}
    coords = []
    for line in lines[customer_data_start_idx:]:
        customer_id = int(line[0])
        x_coord = float(line[1])
        y_coord = float(line[2])
        demand = float(line[3])
        ready_time = float(line[4])
        due_date = float(line[5])
        service_time = float(line[6])
        customers[customer_id] = {
            'id': customer_id,
            'x': x_coord,
            'y': y_coord,
            'demand': demand,
            'ready_time': ready_time,
            'due_date': due_date,
            'service_time': service_time
        }
        coords.append((x_coord, y_coord))
    coords = np.array(coords)
    dist_matrix = np.sqrt(
        np.sum((coords[:, np.newaxis] - coords[np.newaxis, :]) ** 2,
               axis=-1))
    return {
        'instance_name': instance_name,
        'vehicle_max_count': vehicle_max_count,
        'vehicle_capacity': vehicle_capacity,
        'customers': customers,
        'dist_matrix': dist_matrix
    }


def load_config() -> tuple[float, float, int, int, str, str, str]:
    try:
        config = json.load(open('config.json'))
        cp = config['crossing_probability']
        mp = config['mutation_probability']
        p = config['population_size']
        i = config['iterations']
        cm = config['crossing_method']
        sm = config['selection_method']
        mm = config['mutation_method']
        if not (isinstance(cp, (int, float)) and 0 <= cp <= 1):
            raise ValueError(
                "crossing_probability must be a number in range 0–1.")
        if not (isinstance(mp, (int, float)) and 0 <= mp <= 1):
            raise ValueError(
                "mutation_probability must be a number in range 0–1.")
        if not (isinstance(p, int) and p > 0):
            raise ValueError(
                "population_size must be a positive integer.")
        if not (isinstance(i, int) and i > 0):
            raise ValueError(
                "iterations must be a positive integer.")
        if cm not in ("single", "double"):
            raise ValueError(
                "crossing_method must be either 'single' or 'double'.")
        if sm not in ("tournament", "ranking"):
            raise ValueError(
                "selection_method must be either "
                "'tournament' or 'ranking'.")
        if mm not in ("single", "chunk"):
            raise ValueError(
                "mutation_method must be either "
                "'single' or 'chunk'.")
    except Exception as e:
        raise ValueError(f'Error while loading config.json: {e}')
    return cp, mp, p, i, cm, sm, mm
