from typing import Any, Dict, List, Tuple

import numpy as np


class Vehicle:
    def __init__(self, vehicle_id: int, capacity: int, due_date: float):
        self.vehicle_id: int = vehicle_id
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


def optimize_route(vehicle: Vehicle, data: Dict[str, Any]) -> Vehicle:
    """
    :param vehicle: A vehicle, which already contains valid route.
    :param data: Dictionary containing all loaded solomon data.
    :return: vehicle - with improved route (if it was possible).
    The goal of optimize_route algorithm is to optimize a route held
    in a vehicle, by trying to change the order of it and seeing if
    the route is still going to fit within time windows.
    """
    best_route: list[int] = list(vehicle.route)
    best_distance: float = vehicle.total_distance
    is_improved: bool = True

    while is_improved:
        is_improved = False
        # First and last elements are omitted, as route begins and
        # ends always in a home depot.
        for i in range(1, len(best_route) - 2):
            # Second point must be after first point, so that
            # segment [i:j+1] contains elements. Depot is still omitted.
            for j in range(i + 1, len(best_route) - 1):
                # changing order of a route in a following way:
                # - we take every element from best_route,
                # until 'i' index (is not counted in first part).
                # - we take every element, starting from 'i' to 'j',
                # (both included in), and we reverse it.
                # - we take every element, starting from 'j+1' index,
                # to the end of best_route.
                # Finally, we concat all three parts into new route.
                new_route: list[int] = best_route[:i] + best_route[
                    i:j + 1][::-1] + best_route[j + 1:]
                test_v = Vehicle(vehicle.vehicle_id, vehicle.capacity,
                                 vehicle.due_date)
                is_valid = True
                # omitting first element from new_route, as vehicle
                # starts in home depot by default.
                for cust_id in new_route[1:-1]:
                    customer = data['customers'][cust_id]
                    customer['id'] = cust_id
                    if test_v.can_add(customer, data['dist_matrix']):
                        test_v.add_customer(customer,
                                            data['dist_matrix'])
                    else:
                        is_valid = False
                        break

                if is_valid:
                    test_v.close_route(data['dist_matrix'])
                    if test_v.total_distance < best_distance:
                        best_distance = test_v.total_distance
                        best_route = list(test_v.route)
                        is_improved = True

        if is_improved:
            vehicle.route = best_route
            vehicle.total_distance = best_distance

    return vehicle
