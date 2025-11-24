import pandas as pd
import json


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


def load_config() -> tuple[float, float, int, int, str, str]:
    config = json.load(open('config.json'))
    return (config['crossing_probability'], config['mutation_probability'], config['population size'],
            config['iterations'], config['crossing_method'], config['selection_method'])