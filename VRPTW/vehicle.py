from typing import Any, Dict, List, Tuple

import numpy as np


class Vehicle:
    def __init__(self, capacity: int, due_date: float):
        self.capacity: int = capacity
        self.due_date: float = due_date
        self.current_load: int = 0
        self.current_time: float = 0.0
        self.total_distance: float = 0.0
        self.route: List[int] = [0]

    def compute_times(self, customer: Dict[str, Any],
                      dist_matrix: np.ndarray) -> Tuple[
                                                float, float, float]:
        last_id: int = self.route[-1]
        next_id: int = customer['id']
        travel_distance: float = dist_matrix[last_id][next_id]
        arrival_time: float = self.current_time + travel_distance

        start_time: float = max(arrival_time, customer['ready_time'])
        completion_time: float = start_time + customer['service_time']

        return_time: float = completion_time + dist_matrix[next_id][0]
        return arrival_time, return_time, travel_distance

    def can_add(self, customer: Dict[str, Any],
                dist_matrix: np.ndarray) -> bool:
        if self.current_load + customer['demand'] > self.capacity:
            return False

        arrival_time, return_time, _ = self.compute_times(
            customer, dist_matrix)

        if arrival_time > customer['due_date']:
            return False

        if return_time > self.due_date:
            return False
        return True

    def add_customer(self, customer: Dict[str, Any],
                     dist_matrix: np.ndarray) -> None:
        arrival_time, _, travel_distance = self.compute_times(
            customer, dist_matrix)
        start_time = max(arrival_time, customer['ready_time'])
        self.current_time = start_time + customer['service_time']
        self.current_load += customer['demand']
        self.total_distance += travel_distance
        self.route.append(customer['id'])

    def close_route(self, dist_matrix: np.ndarray) -> None:
        if self.route[-1] != 0:
            self.total_distance += dist_matrix[self.route[-1]][0]
            self.route.append(0)


def optimize_route(vehicle: Vehicle, data: Dict[str, Any],
                   force_repair: bool = False) -> Vehicle:
    best_route = list(vehicle.route)
    dist_matrix = data['dist_matrix']
    customers = data['customers']
    capacity = vehicle.capacity
    depot_due_date = vehicle.due_date

    best_distance = vehicle.total_distance \
        if not force_repair else (float('inf'))

    is_improved = True
    while is_improved:
        is_improved = False
        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route) - 1):
                old_edges = (dist_matrix[best_route[i - 1]][
                                 best_route[i]] +
                             dist_matrix[best_route[j]][
                                 best_route[j + 1]])
                new_edges = (dist_matrix[best_route[i - 1]][
                                 best_route[j]] +
                             dist_matrix[best_route[i]][
                                 best_route[j + 1]])
                if new_edges >= old_edges - 1e-9:
                    continue

                new_route = best_route[:i] + best_route[i:j + 1][
                    ::-1] + best_route[j + 1:]

                temp_time = 0.0
                temp_load = 0
                temp_dist = 0.0
                possible = True

                for k in range(1, len(new_route)):
                    prev, curr = new_route[k - 1], new_route[k]
                    cust = customers[curr]

                    d = dist_matrix[prev][curr]
                    arrival = temp_time + d

                    if curr != 0:
                        if (arrival > cust['due_date'] or temp_load +
                                cust['demand'] > capacity):
                            possible = False
                            break

                        temp_time = (max(arrival, cust['ready_time']) +
                                     cust['service_time'])
                    else:
                        if arrival > depot_due_date:
                            possible = False
                            break
                    temp_dist += d

                if possible and temp_dist < best_distance - 1e-9:
                    best_distance = temp_dist
                    best_route = new_route
                    is_improved = True
                    break
            if is_improved:
                break
    vehicle.route = best_route
    vehicle.total_distance = best_distance
    return vehicle
