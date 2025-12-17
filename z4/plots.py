import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from file import read_file


def draw_route(df, order, params):
    x = df.iloc[order]["x"].values
    y = df.iloc[order]["y"].values

    plt.figure(figsize=(8, 8))
    plt.plot(np.append(x, x[0]), np.append(y, y[0]), '-o', color='blue')
    for i, (xi, yi) in enumerate(zip(x, y)):
        if i < len(df):
            plt.text(xi, yi, str(i+1), fontsize=12, color='red')

    plt.xlabel("x")
    plt.ylabel("y")
    param_str = (
        f' dla pliku {params[0]}, parametry:\n'
        f'p_random={params[1]}, alpha={params[2]}, beta={params[3]}, '
        f'iterations={params[4]}, rho={params[5]}, col_size'
        f'={params[6]}.\nDługość trasy: {float(params[7]):.2f}')
    plt.title("Wykres najlepszej trasy" + param_str)
    plt.grid(True)
    plt.show()


def extract_data_from_file_name(file_name: str) -> dict:
    file_data = pd.read_csv(f'results/{file_name}')
    file_name = (file_name.replace('.csv', '')
                 .replace('results-', ''))
    name_parts = file_name.split('-')
    name_parts.pop()
    return {
        'count': name_parts[0],
        'p_random': name_parts[1],
        'alpha': name_parts[2],
        'beta': name_parts[3],
        'iterations': name_parts[4],
        'rho': name_parts[5],
        'col_size': name_parts[6],
        'best': file_data["best"],
        'worst': file_data["worst"],
        'avg': file_data["avg"],
        'time': file_data.iloc[0, -2],
        'best_path': file_data.iloc[0, -1],
        'shortest': file_data.iloc[1, -1],
        'parent_file':
            'A-n32-k5.txt' if name_parts[0] == '32' else 'A-n80-k10.txt'
    }


def extract_data():
    result_folder = "results/"

    data_list = []

    for file in os.listdir(result_folder):
        if not file.endswith(".csv"):
            continue
        data = extract_data_from_file_name(file)
        data["filename"] = file
        data_list.append(data)
    all_data = pd.DataFrame(data_list)
    df32 = read_file('A-n32-k5.txt')
    df80 = read_file('A-n80-k10.txt')
    return all_data, df32, df80


def draw_best_route(data):
    path = []
    parts = data["best_path"].split('->')
    for i in range(len(parts)):
        path.append(int(parts[i]))
    df = df32 if data["count"] == '32' else df80
    params = [data["parent_file"], data["p_random"], data["alpha"],
              data["beta"], data["iterations"], data["rho"],
              data["col_size"], data["shortest"]]
    draw_route(df, path, params)




def draw_comparison_plot(filter_column, value_list, df):
    comparison_avg = {}
    comparison_best = {}
    comparison_worst = {}

    title_part = {
        'p_random': 'parametru p_random',
        'alpha': 'parametru alpha',
        'beta': 'parametru beta',
        'iterations': 'liczby iteracji',
        'rho': 'parametru rho',
        'col_size': 'rozmiaru kolonii',
    }

    for val in value_list:
        filtered_df = df[df[filter_column] == val]
        filtered_df = filtered_df[filtered_df['count'] == '32']


        all_avgs_list = [row['avg'].rename(f"{filter_column}={val} Uruchomienie {i + 1}")
                         for i, (_, row) in enumerate(filtered_df.iterrows())]
        all_best_list = [row['best'].rename(f"{filter_column}={val} Uruchomienie {i + 1}")
                         for i, (_, row) in enumerate(filtered_df.iterrows())]
        all_worst_list = [row['worst'].rename(f"{filter_column}={val} Uruchomienie {i + 1}")
                          for i, (_, row) in enumerate(filtered_df.iterrows())]

        if all_avgs_list:
            all_avgs = pd.concat(all_avgs_list, axis=1)
            comparison_avg[val] = all_avgs.mean(axis=1)

        if all_best_list:
            all_best = pd.concat(all_best_list, axis=1)
            comparison_best[val] = all_best.mean(axis=1)

        if all_worst_list:
            all_worst = pd.concat(all_worst_list, axis=1)
            comparison_worst[val] = all_worst.mean(axis=1)

    if comparison_avg:
        plt.figure(figsize=(14, 6))
        for name, series in comparison_avg.items():
            plt.plot(series, linewidth=2, label=name)
        plt.title(f'Średnie rozwiązania w zależności '
                  f'od {title_part[filter_column]}')
        plt.xlabel('Liczba iteracji')
        plt.ylabel('Długość trasy')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    if comparison_best:
        plt.figure(figsize=(14, 6))
        for name, series in comparison_best.items():
            plt.plot(series, linewidth=2, label=name)
        plt.title(f'Najlepsze rozwiązania w zależności '
                  f'od {title_part[filter_column]}')
        plt.xlabel('Liczba iteracji')
        plt.ylabel('Długość trasy')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    if comparison_worst:
        plt.figure(figsize=(14, 6))
        for name, series in comparison_worst.items():
            plt.plot(series, linewidth=2, label=name)
        plt.title(f'Najgorsze rozwiązania w zależności '
                  f'od {title_part[filter_column]}')
        plt.xlabel('Liczba iteracji')
        plt.ylabel('Długość trasy')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()


df, df32, df80 = extract_data()


draw_comparison_plot('p_random', ['0.01', '0.05', '0.1'], df)
draw_comparison_plot('alpha', ['0.5', '2', '5'], df)
draw_comparison_plot('beta', ['1', '3', '6'], df)
draw_comparison_plot('rho', ['0.1', '0.3', '0.7'], df)
draw_comparison_plot('col_size', ['15', '40', '80'], df)
draw_comparison_plot('iterations', ['100', '300', '600'], df)










