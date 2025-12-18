import json
import os
import pandas as pd


def read_file(filename):
    data = pd.read_csv(filepath_or_buffer=filename,
                       sep=r'\s+',
                       header=None,
                       names=["index", "x", "y"])
    data.set_index('index', inplace=True)
    data.index = data.index - 1
    return data


def load_config():
    try:
        config = json.load(open('config.json'))
        file = config['file']
        p_random = config['p_random']
        alpha = config['alpha']
        beta = config['beta']
        iterations = config['iterations']
        rho = config['rho']
        col_size = config['col_size']
        float_vals_limited = {
            'p_random': p_random,
            'rho': rho
        }
        float_vals_unlimited = {
            'alpha': alpha,
            'beta': beta
        }
        int_vals = {
            'iterations': iterations,
            'col_size': col_size
        }
        if file not in ("A-n32-k5.txt", "A-n80-k10.txt"):
            raise ValueError('Please choose proper file!')
        for name, val in float_vals_limited.items():
            if not (isinstance(val, (int, float)) and 0 <= val <= 1):
                raise ValueError(f'{name} = {val} must be a number '
                                 f'between 0–1')
        for name, val in float_vals_unlimited.items():
            if not (isinstance(val, (int, float)) and val >= 0):
                raise ValueError(f'{name} = {val} must be a number '
                                 f'greater than 0')
        for name, val in int_vals.items():
            if not (isinstance(val, int) and val > 0):
                raise ValueError(f'{name} = {val} must be an integer '
                                 f'greater than 0')
    except Exception as e:
        raise ValueError(f'Error while loading config.json: {e}')
    return file, p_random, alpha, beta, iterations, rho, col_size


def save_run(best, worst, avg, time_elapsed,
             best_path, shortest, file_name_start):
    try:
        result_folder = 'results'
        os.mkdir(result_folder) if not (
            os.path.exists(f'{result_folder}/')) else None
        file_count = sum(1 for file in os.listdir('results') if
                         os.path.isfile(f'results/{file}')
                         and file.startswith(file_name_start)
                         and file.endswith('.csv'))
        file_name = (f'{result_folder}/{file_name_start}-'
                     f'{file_count + 1}.csv')
    except Exception as e:
        print(f'An error occured: {e}')
        return
    try:
        df = pd.DataFrame(
            {
                'best': best,
                'worst': worst,
                'avg': avg
            }
        )
        df['time'] = None
        df['best_path'] = None
        df.loc[0, 'time'] = time_elapsed
        df.loc[0, 'best_path'] = '->'.join(map(str, best_path))
        df.loc[1, 'best_path'] = shortest
        df.to_csv(file_name, index=False)
    except Exception as e:
        print(f'An error occured while saving to {file_name}: {e}')
