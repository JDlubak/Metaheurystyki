import numpy as np


def read_solomon_data(file_path: str) -> dict:
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
        'distance_matrix': dist_matrix
    }
