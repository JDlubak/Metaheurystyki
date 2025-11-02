from z2.funkcje import far_extremum_function, close_extremum_function, smith_simulator

def main():
    print("Wybierz funkcję:")
    print("1 – Przyklad 3)")
    print("2 – Przyklad 4)")
    func_id = int(input("Podaj numer funkcji: "))
    M = int(input("Podaj liczbę iteracji M: "))
    T0 = float(input("Podaj temperaturę początkową T0: "))
    k = float(input("Podaj współczynnik chłodzenia k (np. 0.95): "))

    x, fx = smith_simulator(func_id, M, T0, k)
    print(f"Maksimum globalne jest: {x: .3f} = {fx: .3f}")

main()
