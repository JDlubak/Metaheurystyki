import random

class Ptak:
    def __init__(self, x, y, inercja, stala_poznawcza, stala_spoleczna):
        # Pozycja aktualna
        self.ptak_x = x
        self.ptak_y = y

        # Aktualne przystosowanie cząstki
        self.przystosowanie = float('inf')

        # Prędkość aktualna (inicjalizowana losowo w małym zakresie)
        self.v_x = 0
        self.v_y = 0

        # Najlepsza znana pozycja tej cząstki (personal best)
        self.p_best_x = x
        self.p_best_y = y
        self.p_best_wartosc = float('inf')  # Na start nieskończoność

        # Parametry sterujące ruchem cząstek
        self.inercja = inercja
        self.stala_poznawcza = stala_poznawcza
        self.stala_spoleczna = stala_spoleczna


    def oblicz_przystosowanie(self, func):
        return func(self.ptak_x, self.ptak_y)

    def aktualizuj_predkosc(self, g_best_x, g_best_y):
        r1 = random.random()
        r2 = random.random()

        # Składnik poznawczy (dążenie do własnego najlepszego wyniku)
        vel_cognitive_x = self.stala_poznawcza * r1 * (self.p_best_x - self.ptak_x)
        vel_cognitive_y = self.stala_poznawcza * r1 * (self.p_best_y - self.ptak_y)

        # Składnik społeczny (dążenie do najlepszego wyniku roju)
        vel_social_x = self.stala_spoleczna * r2 * (g_best_x - self.ptak_x)
        vel_social_y = self.stala_spoleczna * r2 * (g_best_y - self.ptak_y)

        # Nowa prędkość
        self.v_x = (self.inercja * self.v_x) + vel_cognitive_x + vel_social_x
        self.v_y = (self.inercja * self.v_y) + vel_cognitive_y + vel_social_y

    def aktualizuj_pozycje(self, bounds):
        self.ptak_x += self.v_x
        self.ptak_y += self.v_y

        # Ograniczenie do zakresu
        min_b, max_b = bounds
        self.ptak_x = max(min_b, min(self.ptak_x, max_b))
        self.ptak_y = max(min_b, min(self.ptak_y, max_b))

    def sprawdz_p_best(self, aktualna_wartosc):
        if aktualna_wartosc < self.p_best_wartosc:
            self.p_best_wartosc = aktualna_wartosc
            self.p_best_x = self.ptak_x
            self.p_best_y = self.ptak_y