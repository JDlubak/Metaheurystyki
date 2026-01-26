import json
import os

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


def load_config() -> tuple[float, float, int, int, str, str]:
    try:
        config = json.load(open('config.json'))
        cp = config['crossing_probability']
        mp = config['mutation_probability']
        p = config['population_size']
        i = config['iterations']
        cm = config['crossing_method']
        sm = config['selection_method']
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
    except Exception as e:
        raise ValueError(f'Error while loading config.json: {e}')
    return cp, mp, p, i, cm, sm


def configurate_parameters(choice):
    if choice == '1':
        return 0.8, 0.2, 200, 1000, "single", "tournament"
    return load_config()


def save_run(instance_name, data, parameters, elapsed_time, vehicles):
    try:
        result_folder = 'wyniki_vrptw'
        os.makedirs(result_folder, exist_ok=True)
        name_start = (f'{instance_name}-{parameters[0]}-{parameters[1]}'
                      f'-{parameters[2]}-{parameters[3]}-'
                      f'{parameters[4]}-{parameters[5]}')
        file_count = sum(1 for file in os.listdir(result_folder) if
                         os.path.isfile(f'{result_folder}/{file}')
                         and file.startswith(name_start)
                         and file.endswith('.csv'))
        file_name = (f'{result_folder}/{name_start}-'
                     f'{file_count + 1}.csv')
    except Exception as e:
        print(f'Wystąpił błąd: {e}')
        return
    try:
        import pandas as pd
        df = pd.DataFrame(
            {
                'best': data[0],
                'best_count': data[1],
                'worst': data[2],
                'worst_count': data[3],
                'avg': data[4],
                'avg_count': data[5],
                'std': data[6],
                'std_count': data[7]
            }
        )
        df['time'] = None
        df.loc[0, 'time'] = elapsed_time

        routes_list = [str(v.route) for v in vehicles]
        if len(routes_list) < len(df):
            routes_list.extend([None] * (len(df) - len(routes_list)))
        elif len(routes_list) > len(df):
            new_rows = pd.DataFrame(
                index=range(len(df), len(routes_list)),
                columns=df.columns)
            df = pd.concat([df, new_rows])
        df['routes'] = routes_list[:len(df)]
        df.to_csv(file_name, index=False)
        print(f"Zapisano wyniki do: {file_name}")
    except Exception as e:
        print(f'Wystąpił błąd podczas zapisu do {file_name}: {e}')
