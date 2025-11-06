def get_parameters() -> tuple[int, int, int, float, float, float]:
    print("Wybierz funkcję:")
    print("1 – Przyklad 3")
    print("2 – Przyklad 4")
    func_id = int(input("Podaj numer funkcji: "))
    epochs = int(input("Podaj liczbę epok: "))
    number_of_attempts = int(input("Podaj ilość prób w epoce: "))
    temperature = float(input("Podaj temperaturę początkową: "))
    alpha = float(
        input("Podaj współczynnik chłodzenia alpha (np. 0.95): "))
    k = float(input("Podaj współczynnik k: "))
    return func_id, epochs, number_of_attempts, temperature, alpha, k


def print_analysis(x, fx, solutions):
    print("----------------------------------------------------------")
    print(f"Znalezione rozwiązanie: f({x}) = {fx}")
    print("Ilość zmian rozwiązania: " + str(len(solutions)))

    x = 0
    fx_best = solutions[0]
    for i in range(len(solutions) - 1):
        if solutions[i + 1] > solutions[i]:
            if fx_best < solutions[i + 1]:
                fx_best = solutions[i + 1]
                x += 1
    print("Ilość zmian rozwiązania na lepsze: " + str(x))
    print("Najlepsza znaleziona wartość funkcji: " + str(fx_best))
    print("----------------------------------------------------------")
