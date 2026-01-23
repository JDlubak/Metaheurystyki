from sa_algorithm.functions import load_function_config
import matplotlib.pyplot as plt
import numpy as np

def drawPlot(function_id, label, title, color):
    config = load_function_config(function_id)
    function = config['func']
    x_min, x_max = config['range']
    x = np.linspace(x_min, x_max, 1000)
    y = [function(x) for x in x]
    plt.figure(figsize=(12, 7))
    plt.plot(x, y, label=label, color=color)
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend()
    plt.show()


def draw_plots():
    drawPlot(1,
             "f(x) - far_extremum",
             "Wykres Funkcji 1: far_extremum_function",
             'blue')
    drawPlot(2,
             "f(x) - close_extremum",
             "Wykres Funkcji 2: close_extremum_function",
             'orange')
    plt.close('all')


def draw_solutions(function_id, solutions: list[tuple[float, float]], x_last:float, y_last:float):
    config = load_function_config(function_id)
    function = config['func']
    x_min, x_max = config['range']
    x = np.linspace(x_min, x_max, 1000)
    y = [function(x) for x in x]

    if function_id == 1:
        color = 'blue'
    else:
        color = 'orange'

    plt.figure(figsize=(12, 7))
    plt.plot(x, y, color=color)

    sol_x = [s[0] for s in solutions]
    sol_y = [s[1] for s in solutions]
    plt.scatter(sol_x, sol_y, color="black", label='Wybierane rozwiązania')

    plt.scatter(x_last, y_last, color="red", s=150, edgecolors="black", linewidths=2, label="Ostatnie rozwiązanie")

    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend()
    plt.show()
