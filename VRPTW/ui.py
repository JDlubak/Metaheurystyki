from plot import plot_all_paths


def main_menu(is_first_call=False):
    if is_first_call:
        print("Witaj w problemie planowania dostaw z uwzględnieniem "
              "okien czasowych (VRPTW)")
        print("Wybierz jedną z opcji:")
        print("1. Uruchom algorytm przy wykorzystaniu "
              "domyślnych parametrów.")
        print("2. Uruchom algorytm przy wykorzystaniu parametrów z "
              "pliku konfiguracyjnego config.json.")
        print("3. Uruchom eksperymenty z wszystkimi kombinacjami "
              "parametrów.")
        print("4. Wyświetl szczegóły dotyczące uruchomienia algorytmu.")
        print("5. Zakończ program.")
    choice = input("Wprowadź numer opcji (1-5): ")
    return choice


def see_details():
    print("--- SZCZEGÓŁY URUCHOMIENIA ALGORYTMU ---")
    print("Korzystamy z implementacji hybrydowej - wspomagamy "
          "algorytm genetyczny lokalnym przeszukiwaniem 2-opt.")
    print("Własności poszczególnych parametrów")
    print("1. Prawdopodobieństwo krzyżowania (crossing_probability). "
          "Określa, jaki procent osobników będzie się krzyżował w "
          "każdej iteracji. Domyślna wartość - 0.8.")
    print("2. Prawdopodobieństwo mutowania (mutation_probability). "
          "Określa, jaki procent osobników będzie mutował w "
          "każdej iteracji. Domyślna wartość - 0.2.")
    print("3. Liczba iteracji (iterations).: Określa, ile iteracji "
          "algorytmu uruchomimy. Domyślna wartość - 500.")
    print("4. Rozmiar populacji (population_size): Określa, "
          "ile osobników znajdzie się w populacji. "
          "Domyślna wartość - 100.")
    print("5. Metoda selekcji (selection_method). Określa, czy do "
          "selekcji będziemy korzystać z turnieju (tournament), "
          "czy z rankingu (ranking)."
          "Domyślnie - tournament.")
    print("6. Metoda krzyżowania: Określa, czy do "
          "krzyżowania będziemy korzystać z krzyżowania "
          "jednopunktowego (single), czy dwupunktowego (double)."
          "Domyślnie - single")
    print("\nMożesz uruchomić algorytm z domyślnymi parametrami "
          "(opcja 1), załadować je z pliku config.json (opcja 2) lub "
          "uruchomić eksperymenty z różnymi kombinacjami parametrów. "
          "(opcja 3)")
    print("Do eksperymentów zostaną użyte następujące wartości "
          "parametrów:")
    print("- Prawdopodobieństwo krzyżowania: 0.6, 0.8, 1.0")
    print("- Prawdopodobieństwo krzyżowania: 0.05, 0.1, 0.2")
    print("- Rozmiar populacji - 40, 100, 200")
    print("- Liczba iteracji - 100, 300, 1000")
    print("- Metody krzyżowania i selekcji - wszystkie 4.")
    print("\nMamy zatem 3 x 3 x 3 x 3 x 4 = 324 kombinacje do "
          "przetestowania, każda kombinacja zostanie przetestowana 5 "
          "razy dla trzech plików, co daje łącznie 4860 "
          "uruchomień algorytmu.")
    print("Wybierz odpowiednią opcję z menu głównego.")
    return


def menu_vrptw(crossing_method, selection_method, crossing_probability,
               mutation_probability, population_size, iterations):
    print("--- VRPTW - Algorytm genetyczny + 2-opt ---")
    print(f"\nParametry:")
    print(f"- Metoda krzyżowania: {crossing_method}")
    print(f"- Metoda selekcji: {selection_method}")
    print(f"- Prawdopodobieństwo krzyżowania: {crossing_probability}")
    print(f"- Prawdopodobieństwo mutacji: {mutation_probability}")
    print(f"- Rozmiar populacji: {population_size}")
    print(f"- Ilośc iteracji: {iterations}\n")

    print("Wybierz dane:")
    print("1. grupa R1.. / R2.. – przypadki losowe.")
    print("2. grupa C1.. / C2.. – przypadki skupione (klastry).")
    print("3. grupa RC1.. / RC2.. – mieszanka klastrów i "
          "rozmieszczenia losowego.")


def see_results(best, elapsed_time, data):
    distance = best['value'] % 10000
    vehicles = best['value'] // 10000
    print("\n--- WYNIKI KOŃCOWE ---")
    print(f"Długość najlepszej trasy: {distance:.3f}")
    print(f"Liczba pojazdów: {vehicles:.0f}")
    print(f"Trasy wszystkich pojazdów:")
    routes = []
    for i, vehicle in enumerate(best['vehicles']):
        print(f"{i + 1}. {vehicle.route}")
        routes.append(vehicle.route)
    print(f"Czas wykonania: {elapsed_time:.4f} sekund\n")
    plot_all_paths(data, routes)
    print("Utworzono wykres obrazujący trasy.")
    input("Naciśnij Enter, aby kontynuować...")
    return
