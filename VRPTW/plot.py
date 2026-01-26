import matplotlib.pyplot as plt


def plot_all_paths(data, routes):
    plt.figure(figsize=(12, 10))

    depot = data['customers'][0]
    plt.scatter(depot['x'], depot['y'], c='red', marker='s', s=100,
                label='Baza', zorder=5)

    cust_x = [c['x'] for id, c in data['customers'].items() if id != 0]
    cust_y = [c['y'] for id, c in data['customers'].items() if id != 0]
    plt.scatter(cust_x, cust_y, c='blue', marker='o', s=30, alpha=0.6,
                label='Klienci')

    cmap = plt.get_cmap('tab20')

    for i, route in enumerate(routes):
        color = cmap(i % 20)

        route_x = [data['customers'][node]['x'] for node in route]
        route_y = [data['customers'][node]['y'] for node in route]

        plt.plot(route_x, route_y, color=color,
                 linewidth=2, alpha=0.8)

    plt.title(
        f"Wizualizacja tras VRPTW - Instancja: {data['instance_name']} "
        f"({len(routes)} pojazdów)")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))

    plt.tight_layout()
    plt.show()
