from functions import load_function_config
from PSO import PSO

def main():
    print("--- ALGORYTM ROJU CZĄSTEK (PSO) ---")
    print("Wybierz funkcję do optymalizacji:")
    print("1. Funkcja Beale'a")
    print("2. Funkcja Himmelblau")

    try:
        wybor = int(input("Twój wybór (1 lub 2): "))
        config = load_function_config(wybor)

        print(f"\nWybrano: {config['name']}")
        print(f"Zakres poszukiwań: {config['range']}")

        # Utworzenie i uruchomienie algorytmu
        algorytm = PSO(config, liczba_czastek=50, iteracje=100)
        x, y, val, time = algorytm.uruchom()

        print("\n--- WYNIKI KOŃCOWE ---")
        print(f"Znalezione minimum w punkcie: ({x:.4f}, {y:.4f})")
        print(f"Wartość funkcji: {val:.6f}")
        print(f"Czas wykonania: {time:.4f} sekund\n")

    except ValueError as e:
        print(f"Błąd: {e}")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")


if __name__ == "__main__":
    while True:
        main()