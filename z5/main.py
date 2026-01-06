import sys

from experiments import przeprowadz_eksperymenty
from file import konfiguruj_parametry
from functions import load_function_config
from PSO import PSO
from ui import (menu_glowne, menu_pso, wyswietl_podsumowanie,
                wyswietl_szczegoly)


def wybierz_sposob_uruchomienia():
    pierwsze_wywolanie = True
    while True:
        sposob_uruchomienia = menu_glowne(
            czy_pierwsze_wywolanie=pierwsze_wywolanie)
        pierwsze_wywolanie = False
        if sposob_uruchomienia in {'1', '2', '3'}:
            break
        elif sposob_uruchomienia == '4':
            wyswietl_szczegoly()
        elif sposob_uruchomienia == '5':
            print("Zakończenie programu.")
            sys.exit(0)
        else:
            print("Niepoprawny wybór. Spróbuj ponownie. ", end='')
    return sposob_uruchomienia


def main(parametry):
    liczba_czastek = parametry[0]
    iteracje = parametry[1]
    inercja = parametry[2]
    stala_poznawcza = parametry[3]
    stala_spoleczna = parametry[4]
    menu_pso(liczba_czastek, iteracje, inercja, stala_poznawcza,
             stala_spoleczna)
    try:
        wybor = int(input("Twój wybór (1 lub 2): "))
        config = load_function_config(wybor)

        print(f"\nWybrano: {config['name']}")
        print(f"Zakres poszukiwań: {config['range']}")

        # Utworzenie i uruchomienie algorytmu
        algorytm = PSO(config,
                       liczba_czastek=liczba_czastek,
                       iteracje=iteracje,
                       inercja=inercja,
                       stala_spoleczna=stala_spoleczna,
                       stala_poznawcza=stala_poznawcza)
        x, y, val, time = algorytm.uruchom(komunikaty=True)
        wyswietl_podsumowanie(time, x, y, val)

    except ValueError as e:
        print(f"Błąd: {e}")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")


if __name__ == "__main__":
    sposob_uruchomienia = wybierz_sposob_uruchomienia()
    if sposob_uruchomienia == '3':
        przeprowadz_eksperymenty()
    else:
        parametry = konfiguruj_parametry(sposob_uruchomienia)
        while True:
            main(parametry)
