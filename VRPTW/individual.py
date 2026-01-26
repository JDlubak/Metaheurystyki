import random
from vehicle import Vehicle, optimize_route
from VRPTW.file import read_solomon_data


class Individual:
    def __init__(self, number_of_clients: int, order: list[int] = None):
        self.vehicles = []
        self.value = 0
        if order is None:
            self.order = list(range(1, number_of_clients + 1))
            random.shuffle(self.order)
        else:
            self.order = order

    def create_vehicles(self, data: dict):
        self.vehicles = []
        next_id = 1
        due_date = data['customers'][0]['due_date']
        capacity = data['vehicle_capacity']
        dist_matrix = data['dist_matrix']
        vehicle = Vehicle(next_id, capacity, due_date)
        for client in self.order:
            customer = data['customers'][client]
            if vehicle.can_add(customer, dist_matrix):
                vehicle.add_customer(customer, dist_matrix)
            else:
                vehicle.close_route(dist_matrix)
                vehicle = optimize_route(vehicle, data)
                self.vehicles.append(vehicle)
                next_id += 1
                vehicle = Vehicle(next_id, capacity, due_date)
                vehicle.add_customer(customer, dist_matrix)

    def evaluate(self):
        self.value = 0
        for vehicle in self.vehicles:
            self.value += 10000
            self.value += vehicle.total_distance


data = read_solomon_data('solomon-100/In/c101.txt')
ind = Individual(100)
ind.create_vehicles(data)
for vehicle in ind.vehicles:
    print(vehicle.route)
