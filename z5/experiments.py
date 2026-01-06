from functions import load_function_config
from itertools import product
from PSO import PSO


def przeprowadz_eksperymenty():
    funkcje = [1, 2]
    liczby_czastek = [20, 50, 100]
    liczby_iteracji = [50, 100, 200]
    inercje = [0.3, 0.5, 0.7]
    stale_poznawcze = [1.0, 1.5, 2.0]
    stale_spoleczne = [0.5, 1.0, 1.5]
    licznik = 0
    for f in funkcje:
        config = load_function_config(f)
        for c, iter, iner, sp, ss in (product(liczby_czastek,
                                              liczby_iteracji, inercje,
                                              stale_poznawcze,
                                              stale_spoleczne)):
            for _ in range(5):
                algorytm = PSO(config,
                               liczba_czastek=c,
                               iteracje=iter,
                               inercja=iner,
                               stala_spoleczna=ss,
                               stala_poznawcza=sp)
                algorytm.uruchom(komunikaty=False)
                licznik = licznik + 1
    print(f'Przeprowadzono pomyślnie {licznik} eksperymentów')
    return
