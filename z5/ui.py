def menu_glowne(czy_pierwsze_wywolanie=False):
    if czy_pierwsze_wywolanie:
        print("Witaj w programie optymalizacji rojem cząstek (PSO)!")
        print("Wybierz jedną z opcji:")
        print("1. Uruchom algorytm przy wykorzystaniu "
              "domyślnych parametrów.")
        print("2. Uruchom algorytm przy wykorzystaniu parametrów z "
              "pliku konfiguracyjnego config.json.")
        print("3. Uruchom eksperymenty z wszystkimi kombinacjami "
              "parametrów.")
        print("4. Wyświetl szczegóły dotyczące uruchomienia algorytmu.")
        print("5. Zakończ program.")
    wybor = input("Wprowadź numer opcji (1-5): ")
    return wybor


def wyswietl_szczegoly():
    print("--- SZCZEGÓŁY URUCHOMIENIA ALGORYTMU ---")
    print("W algorytmie PSO (Particle Swarm Optimization) mamy 5 "
          "konfigurowalnych parametrów:")
    print("1. Liczba cząstek: Określa, ile cząstek będzie "
          "uczestniczyć w optymalizacji. Domyślna wartość - 50.")
    print("2. Liczba iteracji: Określa, ile razy cząstki będą "
          "aktualizować swoje pozycje. Domyślna wartość - 100.")
    print("3. Inercja: Współczynnik wpływający na prędkość cząstek. "
          "Wartość z przedziału [0, 1]. Domyślna wartość - 0.5.")
    print("4. Stała poznawcza: Współczynnik wpływający na "
          "dążenie cząstek do ich własnych najlepszych znanych pozycji."
          " Wartość z przedziału [0, 2]. Domyślna wartość - 1.5.")
    print("5. Stała społeczna: Współczynnik wpływający na "
          "dążenie cząstek do najlepszej znanej pozycji w roju. "
          "Wartość większa lub równa 0. Domyślna wartość - 1.5.")
    print("\nMożesz uruchomić algorytm z domyślnymi parametrami "
          "(opcja 1), załadować je z pliku config.json (opcja 2) lub "
          "uruchomić eksperymenty z różnymi kombinacjami parametrów. "
          "(opcja 3)")
    print("Do eksperymentów zostaną użyte następujące wartości "
          "parametrów:")
    print("- Liczba cząstek: 10, 50, 100")
    print("- Liczba iteracji: 100, 200, 500")
    print("- Inercja: 0.2, 0.5, 0.8")
    print("- Stała poznawcza: 0.3, 1.2, 2.0")
    print("- Stała społeczna: 0.3, 1.2, 2.0")
    print("\nMamy zatem 3 x 3 x 3 x 3 x 3 = 243 kombinacje do "
          "przetestowania, każda kombinacja zostanie przetestowana 5 "
          "razy dla obu funkcji, co daje łącznie 2430 uruchomień "
          "algorytmu.")
    print("Wybierz odpowiednią opcję z menu głównego.")
    return


def wyswietl_podsumowanie(time, x, y, val):
    print("\n--- WYNIKI KOŃCOWE ---")
    print(f"Znalezione minimum w punkcie: ({x:.4f}, {y:.4f})")
    print(f"Wartość funkcji: {val:.6f}")
    print(f"Czas wykonania: {time:.4f} sekund\n")
    input("Naciśnij Enter, aby kontynuować...")
    return


def menu_pso(liczba_czastek, iteracje, inercja, stala_poznawcza,
             stala_spoleczna):
    print("--- ALGORYTM ROJU CZĄSTEK (PSO) ---")
    print(f"\nParametry:")
    print(f"- Liczba cząstek: {liczba_czastek}")
    print(f"- Liczba iteracji: {iteracje}")
    print(f"- Inercja: {inercja}")
    print(f"- Stała poznawcza: {stala_poznawcza}")
    print(f"- Stała społeczna: {stala_spoleczna}\n")

    print("Wybierz funkcję do optymalizacji:")
    print("1. Funkcja Beale'a")
    print("2. Funkcja Himmelblau")
    return
