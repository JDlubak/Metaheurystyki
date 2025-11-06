import sys


def get_parameters() -> tuple[int, int, int, float, float, float]:
    print("Wybierz funkcję:")
    print("1 – Przyklad 3")
    print("2 – Przyklad 4")
    try:
        while True:
            func_id = int(input("Podaj numer funkcji: "))
            if func_id in [1, 2]:
                break
        epochs = int(input("Podaj liczbę epok: "))
        number_of_attempts = int(input("Podaj ilość prób w epoce: "))
        temperature = float(input("Podaj temperaturę początkową: "))
        alpha = float(
            input("Podaj współczynnik chłodzenia alpha (np. 0.95): "))
        k = float(input("Podaj współczynnik k: "))
    except ValueError:
        print("Błędny parametr wejściowy!")
        sys.exit(1)
    return func_id, epochs, number_of_attempts, temperature, alpha, k


def print_analysis(x, fx, solutions, time):
    print("----------------------------------------------------------")
    print(f"Znalezione rozwiązanie: f({x}) = {fx}")
    print("Ilość zmian rozwiązania: " + str(len(solutions)))

    x = 0
    fx_best = solutions[0][1]
    for i in range(len(solutions) - 1):
        if solutions[i + 1][1] > solutions[i][1]:
            if fx_best < solutions[i + 1][1]:
                fx_best = solutions[i + 1][1]
                x += 1
    print("Ilość zmian rozwiązania na lepsze: " + str(x))
    print("Najlepsza znaleziona wartość funkcji: " + str(fx_best))
    print("Czas trwania poszukiwań: " + str(time))
    print("----------------------------------------------------------")
