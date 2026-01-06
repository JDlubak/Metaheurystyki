import random
import time

import numpy as np

from file import zapisz_wartosci
from wielki_silny_ptak import Ptak


class PSO:
    def __init__(self, func_config, liczba_czastek, iteracje,
                 inercja, stala_poznawcza, stala_spoleczna):
        self.func = func_config['func']
        self.numer_funkcji = func_config["number"]
        self.bounds = func_config['range']
        self.liczba_czastek = liczba_czastek
        self.iteracje = iteracje

        # Parametry roju
        self.inercja = inercja
        self.stala_poznawcza = stala_poznawcza
        self.stala_spoleczna = stala_spoleczna

        # Parametr do zapobiegania przedwczesnemu skupieniu w jednym obszarze przestrzeni zaraz po inicjalizacji
        # Jak blisko muszą być cząstki, żeby uznać, że "utknęły"
        self.prog_skupienia = 2
        self.procent_restartu = 0.8

        # Inicjalizacja roju
        self.roj = []
        for _ in range(liczba_czastek):
            # W przypadku wybranych funckji granice dla x i y są takie same, więc możemy tak zrobić
            # bo w sumie nie dodawałem oddzielnych granic dla x i y tylko jest jeden range
            start_x = random.uniform(self.bounds[0], self.bounds[1])
            start_y = random.uniform(self.bounds[0], self.bounds[1])
            p = Ptak(start_x, start_y, self.inercja, self.stala_poznawcza, self.stala_spoleczna)
            self.roj.append(p)

        # Global Best (g_best)
        self.g_best_x = 0
        self.g_best_y = 0
        self.g_best_wartosc = float('inf')

    # Na podstawie odchylenia standardowego sprawdzamy, czy cząstki nie są zbyt blisko siebie na początku
    def czy_roj_skupiony(self):
        x_positions = [p.ptak_x for p in self.roj]
        y_positions = [p.ptak_y for p in self.roj]

        std_x = np.std(x_positions)
        std_y = np.std(y_positions)

        return std_x < self.prog_skupienia and std_y < self.prog_skupienia

    def reset_czastek(self):
        ile_zresetowac = int(self.liczba_czastek * self.procent_restartu)
        licznik = 0
        for ptak in self.roj:
            licznik += 1
            if licznik <= ile_zresetowac:
                ptak.ptak_x = random.uniform(self.bounds[0], self.bounds[1])
                ptak.ptak_y = random.uniform(self.bounds[0], self.bounds[1])

    def uruchom(self, komunikaty):
        najlepsze = []
        srednie = []
        najgorsze = []
        mediany = []
        odchylenia = []

        if komunikaty:
            print(f"Rozpoczynam optymalizację rojem {self.liczba_czastek} cząstek...")
        czas_startu = time.time()
        while self.czy_roj_skupiony():
            self.reset_czastek()

        for i in range(self.iteracje):
            for ptak in self.roj:
                # 1. Oblicz wartość funkcji
                wynik = ptak.oblicz_przystosowanie(self.func)

                # 2. Aktualizuj p_best (najlepszy wynik osobisty)
                ptak.sprawdz_p_best(wynik)

                # 3. Aktualizuj g_best (najlepszy wynik globalny)
                if wynik < self.g_best_wartosc:
                    self.g_best_wartosc = wynik
                    self.g_best_x = ptak.ptak_x
                    self.g_best_y = ptak.ptak_y

            # 4. Ruch cząstek (aktualizacja prędkości i pozycji)
            for ptak in self.roj:
                ptak.aktualizuj_predkosc(self.g_best_x, self.g_best_y)
                ptak.aktualizuj_pozycje(self.bounds)

            # Wypisz status co 10 iteracji
            if (i + 1) % 10 == 0 and komunikaty:
                print(f"Iteracja {i + 1}: Najlepszy wynik = {self.g_best_wartosc:.5f}")

            # Zapisz najlepszy, średni, najgorszy wynik z iteracji
            # oraz medianę i odchylenie standardowe
            wartosci = [ptak.przystosowanie for ptak in self.roj]
            najlepsze.append(min(wartosci))
            srednie.append(sum(wartosci) / len(wartosci))
            najgorsze.append(max(wartosci))
            mediany.append(np.median(wartosci))
            odchylenia.append(np.std(wartosci))
        czas_konca = time.time()
        czas_dzialania = czas_konca - czas_startu

        parametry = [self.numer_funkcji, self.liczba_czastek, self.iteracje,
                     self.inercja, self.stala_poznawcza,
                     self.stala_spoleczna]
        zapisz_wartosci(najlepsze, srednie, najgorsze, mediany,
                        odchylenia, parametry, czas_dzialania)

        return self.g_best_x, self.g_best_y, self.g_best_wartosc, czas_dzialania
