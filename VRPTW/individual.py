import random

from vehicle import optimize_route, Vehicle


class Individual:
    def __init__(self, number_of_clients: int, order: list[int] = None):
        self.vehicles = []
        self.value = 0
        if order is None:
            self.order = list(range(1, number_of_clients + 1))
            random.shuffle(self.order)
        else:
            self.order = order
        self.adaptation = 0
        self.evaluated = False

    def create_vehicles(self, data: dict):
        if self.evaluated:
            return
        self.vehicles = []
        due_date = data['customers'][0]['due_date']
        capacity = data['vehicle_capacity']
        dist_matrix = data['dist_matrix']
        vehicle = Vehicle(capacity, due_date)
        for client in self.order:
            customer = data['customers'][client]
            if vehicle.can_add(customer, dist_matrix):
                vehicle.add_customer(customer, dist_matrix)
            else:
                vehicle.close_route(dist_matrix)
                self.vehicles.append(vehicle)

                vehicle = Vehicle(capacity, due_date)
                vehicle.add_customer(customer, dist_matrix)

        vehicle.close_route(dist_matrix)
        self.vehicles.append(vehicle)

    def evaluate(self, data: dict):
        if self.evaluated:
            return
        self.value = 0
        for vehicle in self.vehicles:
            vehicle = optimize_route(vehicle, data)
            self.value += 10000
            self.value += vehicle.total_distance
        updated_order = []
        for v in self.vehicles:
            updated_order.extend([cid for cid in v.route if cid != 0])
        self.order = updated_order
        self.evaluated = True
