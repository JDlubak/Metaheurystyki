from z2.funkcje import sa_algorithm
from z2.plot import drawPlots


def main():
    drawPlots()
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
