import pandas as pd
from handle_population import create_population
from selection import selection_algorithm

def load_data() -> dict:
    data = pd.read_csv('problem plecakowy dane CSV tabulatory.csv',
                       sep='\t')
    data = data.rename(columns={'Nazwa': 'Name',
                                'Waga (kg)': 'Weight',
                                'Wartość (zł)': 'Value'})
    data['Weight'] = data['Weight'].str.replace(' ', '').astype(int)
    data['Value'] = data['Value'].str.replace(' ', '').astype(int)
    items = data.set_index('Numer').to_dict('index')
    return items


item_list = load_data()
population = create_population(item_list, 100)
selection = selection_algorithm(population, 20, 'roulette')
for item in selection:
    print(item)



