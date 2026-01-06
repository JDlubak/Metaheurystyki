import json
import os


def zaladuj_parametry():
    pola = {"funkcja", "liczba_czastek", "iteracje", "inercja",
            "stala_poznawcza", "stala_spoleczna", "prog_skupienia"}

    try:
        parametry = json.load(open('config.json'))
        liczba_czastek = parametry['liczba_czastek']
        iteracje = parametry['iteracje']
        inercja = parametry['inercja']
        stala_poznawcza = parametry['stala_poznawcza']
        stala_spoleczna = parametry['stala_spoleczna']

        bledy = []

        if not (isinstance(liczba_czastek, int) and liczba_czastek > 0):
            bledy.append('Liczba cząstek musi być '
                         'liczbą całkowitą większą od 0.')
        if not (isinstance(iteracje, int) and iteracje > 0):
            bledy.append('Liczba iteracji musi być '
                         'liczbą całkowitą większą od 0.')
        if not (isinstance(inercja, (int, float))
                and 0 <= inercja <= 1):
            bledy.append('Inercja musi być liczbą '
                         'z przedziału od 0 do 1.')
        if not (isinstance(stala_poznawcza, (int, float))
                and 0 <= stala_poznawcza <= 2):
            bledy.append('Stała poznawcza musi być liczbą '
                         'z przedziału od 0 do 2.')
        if not (isinstance(stala_spoleczna, (int, float))
                and stala_spoleczna >= 0):
            # zgodnie z wykładem, nie ma tu górnego ograniczenia
            bledy.append('Stała społeczna musi być liczbą '
                         'większą lub równą 0.')
        dodatkowe_pola = set(parametry.keys()) - pola
        if dodatkowe_pola:
            bledy.append(f'Niepoprawne pola: '
                         f'{", ".join(dodatkowe_pola)}')
        if bledy:
            raise ValueError(' '.join(bledy))
    except json.JSONDecodeError as e:
        raise ValueError(f'Niepoprawny format pliku config.json: {e}')
    except KeyError as e:
        raise ValueError(f'Brakujące pole: {e}')
    except Exception as e:
        raise ValueError(f'Błąd ładowania config.json: {e}')

    return (liczba_czastek, iteracje, inercja,
            stala_poznawcza, stala_spoleczna)


def konfiguruj_parametry(sposob_uruchomienia):
    if sposob_uruchomienia == '1':
        return 50, 100, 0.5, 1.5, 1.5
    return zaladuj_parametry()


def zapisz_wartosci(najlepsze, srednie, najgorsze,
                    mediany, odchylenia, parametry, czas):
    try:
        katalog = 'wyniki_PSO'
        os.makedirs(katalog, exist_ok=True)
        start_nazwy = (f'{parametry[0]}-{parametry[1]}-{parametry[2]}-'
                       f'{parametry[3]}-{parametry[4]}-'
                       f'{parametry[5]}')
        liczba_plikow = sum(1 for file in os.listdir(katalog) if
                            os.path.isfile(f'{katalog}/{file}')
                            and file.startswith(start_nazwy)
                            and file.endswith('.csv'))
        nazwa_pliku = (f'{katalog}/{start_nazwy}-'
                       f'{liczba_plikow + 1}.csv')
    except Exception as e:
        print(f'Wystąpił błąd: {e}')
        return
    try:
        import pandas as pd
        df = pd.DataFrame(
            {
                'najlepsze': najlepsze,
                'najgorsze': najgorsze,
                'srednie': srednie,
                'mediany': mediany,
                'odchylenia': odchylenia
            }
        )
        df['czas'] = None
        df.loc[0, 'czas'] = czas
        df.to_csv(nazwa_pliku, index=False)
    except Exception as e:
        print(f'Wystąpił błąd podczas zapisu do {nazwa_pliku}: {e}')
