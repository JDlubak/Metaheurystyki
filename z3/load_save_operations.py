import os

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
    return (config['crossing_probability'], config['mutation_probability'],
            config['population size'], config['iterations'],
            config['crossing_method'], config['selection_method'])


def save_iteration_data(pop: list[dict], best: list[dict], worst: list[dict],
                        worst_with_zero: list[dict], avg: list[float]) -> None:
    values = [ind['Value'] for ind in pop]
    max_index = values.index(max(values))
    non_zero_values = [v for v in values if v > 0]
    if non_zero_values:
        min_index = values.index(min(non_zero_values))
    else:
        min_index = values.index(min(values))
    min_index_with_zero = values.index(min(values))
    avg_value = sum(values) / len(values)
    best.append(pop[max_index].copy())
    worst.append(pop[min_index].copy())
    worst_with_zero.append(pop[min_index_with_zero].copy())
    avg.append(avg_value)


def data_to_csv(best: list[dict], worst: list[dict], worst_with_zero: list[dict], avg: list[float],
                total_time: float) -> None:
    try:
        (crossing_probability, mutation_probability, population_size,
         iterations, crossing_method, selection_method) = load_config()
    except Exception as e:
        print(f'Wystąpił błąd: {e}')
        return
    try:
        file_name_start = (f'results-{crossing_method}-{selection_method}-{iterations}-'
                           f'{population_size}-{crossing_probability}-{mutation_probability}')
        os.mkdir('results') if not os.path.exists('results/') else None
        file_count = sum(1 for file in os.listdir('results') if os.path.isfile(file)
                         and file.startswith(file_name_start)
                         and file.endswith('.csv'))
        file_name = f'results/{file_name_start}-{file_count + 1}.csv'
    except Exception as e:
        print(f'Wystąpił błąd: {e}')
        return
    try:
        df = pd.DataFrame(
            {'Best_Name': [b['Name'] for b in best],
             'Best_Value': [b['Value'] for b in best],
             'Worst_Name': [w['Name'] for w in worst],
             'Worst_Value': [w['Value'] for w in worst],
             'Worst_With_Zero': [w['Name'] for w in worst_with_zero],
             'Worst_Value_With_Zero': [w['Value'] for w in worst_with_zero],
             'Avg': avg})
        df['Total_Time'] = [total_time] + [None] * (len(df) - 1)
        df.to_csv(file_name, index=False)
    except Exception as e:
        print(f'Wystąpił błąd przy zapisie do pliku {file_name}: {e}')
