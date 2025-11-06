from z2.funkcje import sa_algorithm
from z2.plot import drawPlots


def main():
    drawPlots()
    print("Wybierz funkcję:")
    print("1 – Przyklad 3)")
    print("2 – Przyklad 4)")
    func_id = int(input("Podaj numer funkcji: "))
    M = int(input("Podaj liczbę iteracji M: "))
    T0 = float(input("Podaj temperaturę początkową T0: "))
    alpha = float(input("Podaj współczynnik chłodzenia alpha (np. 0.95): "))
    k = float(input("Podaj współczynnik k: "))

    x, fx = sa_algorithm(func_id, M, T0, alpha,1, k)
    print(f"Maksimum globalne jest: {x: .3f} = {fx: .3f}")


main()
