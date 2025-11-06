import matplotlib.pyplot as plt
import numpy as np
from z2.funkcje import far_extremum_function, close_extremum_function, sa_algorithm


def plot_functions():
    x_far = np.linspace(-150, 150, 1000)
    y_far = [far_extremum_function(x) for x in x_far]

    plt.figure(figsize=(12, 7))
    plt.plot(x_far, y_far, label="f(x) - far_extremum")
    plt.title("Wykres Funkcji 1: far_extremum_function")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend()
    plt.show()
    x_close = np.linspace(-1, 2, 1000)
    y_close = [close_extremum_function(x) for x in x_close]
    plt.figure(figsize=(12, 7))
    plt.plot(x_close, y_close, label="f(x) - close_extremum", color='orange')
    plt.title("Wykres Funkcji 2: close_extremum_function")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend()
    plt.show()
    plt.close('all')


def main():
    #plot_functions()

    print("Wybierz funkcję:")
    print("1 – Przyklad 3")
    print("2 – Przyklad 4")
    func_id = int(input("Podaj numer funkcji: "))
    epochs = int(input("Podaj liczbę epok: "))
    number_of_attempts = int(input("Podaj ilość prób w epoce: "))
    temperature = float(input("Podaj temperaturę początkową: "))
    alpha = float(input("Podaj współczynnik chłodzenia alpha (np. 0.95): "))
    k = float(input("Podaj współczynnik k: "))

    x, fx, solutions = sa_algorithm(func_id, epochs, temperature, alpha, number_of_attempts, k)
    print(f"Maksimum globalne jest: {x: .3f} = {fx: .3f}")
    print(len(solutions))

    x = 0
    fx_best = solutions[0]
    for i in range(len(solutions) - 1):
        if solutions[i + 1] > solutions[i]:
            if fx_best < solutions[i + 1]:
                fx_best = solutions[i + 1]
                x += 1

    print(x)
    print(fx_best)

while True:
    main()

