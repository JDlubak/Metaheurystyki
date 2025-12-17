import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from file import read_file


def draw_route(ax, df, order, params, title_for_plot, filter_column):
    x = df.iloc[order]["x"].values
    y = df.iloc[order]["y"].values

    ax.plot(np.append(x, x[0]), np.append(y, y[0]), '-o', color='blue')
    for i, (xi, yi) in enumerate(zip(x, y)):
        if i < len(df):
            ax.text(xi, yi, str(i+1), fontsize=12, color='red')

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    param_parts = []
    for key, value in params.items():
        if key in ('shortest', filter_column):
            continue
        param_parts.append(f"{key}={value}")
    param_str = ", ".join(param_parts)
    param_str += f"\nDługość trasy: {float(params['shortest']):.2f}"
    ax.set_title(f'Najlepsza trasa {title_for_plot}, parametry:\n '
                 f'{param_str}')
    ax.grid(True)


def draw_best_route(ax, data, df_number, title_for_plot, filter_column):
    path = [int(p) for p in data["best_path"].split('->')]
    params = {
        'p_random': data["p_random"],
        'alpha': data["alpha"],
        'beta': data["beta"],
        'iterations': data["iterations"],
        'rho': data["rho"],
        'col_size': data["col_size"],
        'shortest': data["shortest"]
    }
    draw_route(ax, df_number, path, params, title_for_plot,
               filter_column)


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


def draw_comparison_plot(filter_column, value_list, df, df_number):
    title_part = {
        'p_random': 'parametru p_random',
        'alpha': 'parametru alpha',
        'beta': 'parametru beta',
        'iterations': 'liczby iteracji',
        'rho': 'parametru rho',
        'col_size': 'rozmiaru kolonii',
    }
    problem_size = len(df_number)
    main_df = df[df['count'] == str(problem_size)]
    main_df = main_df[main_df['beta'].isin(['10'])]

    comparison_avg = {}
    comparison_best = {}
    comparison_worst = {}

    fig, axes = plt.subplots(3, 2, figsize=(12, 16))
    axes_flat = axes.flatten()
    title_end = "plik A-n32-k5.txt" if problem_size == 32 \
        else "plik A-n80-k10.txt"

    fig.suptitle(f'Wpływ {title_part[filter_column]} '
                 f'na wyniki algorytmu ACO - {title_end}', fontsize=16)

    for (i, val) in enumerate(value_list):
        filtered_df = main_df[main_df[filter_column] == val]
        best_row = filtered_df.loc[pd.to_numeric(filtered_df['shortest'], errors='coerce').idxmin()]
        title_for_plot = f'dla {title_part[filter_column]} {val}'
        ax = axes_flat[i]
        draw_best_route(ax, best_row, df_number, title_for_plot,
                        filter_column)

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

    ax = axes_flat[3]
    if comparison_best:
        for name, series in comparison_best.items():
            ax.plot(series, linewidth=2, label=name)
        ax.set_title(
            f'Najlepsze rozwiązania')
        ax.set_xlabel('Liczba iteracji')
        ax.set_ylabel('Długość trasy')
        ax.grid(True)
        ax.legend()
    else:
        ax.text(0.5, 0.5, 'Brak danych dla najlepszych', ha='center',
                va='center')
        ax.axis('off')

    ax = axes_flat[4]
    if comparison_avg:
        for name, series in comparison_avg.items():
            ax.plot(series, linewidth=2, label=name)
        ax.set_title(f'Średnie rozwiązania')
        ax.set_xlabel('Liczba iteracji')
        ax.set_ylabel('Długość trasy')
        ax.grid(True)
        ax.legend()
    else:
        ax.text(0.5, 0.5, 'Brak danych dla średnich', ha='center', va='center')
        ax.axis('off')

    ax = axes_flat[5]
    if comparison_worst:
        for name, series in comparison_worst.items():
            ax.plot(series, linewidth=2, label=name)
        ax.set_title(
            f'Najgorsze rozwiązania')
        ax.set_xlabel('Liczba iteracji')
        ax.set_ylabel('Długość trasy')
        ax.grid(True)
        ax.legend()
    else:
        ax.text(0.5, 0.5, 'Brak danych dla najgorszych', ha='center',
                va='center')
        ax.axis('off')

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    values_str = "_".join(value_list)

    filename = (
        f"aco_{problem_size}_"
        f"{filter_column}_"
        f"{values_str}.png"
    )
    filepath = os.path.join('plots', filename)
    plt.savefig(filepath, dpi=300, bbox_inches="tight")
    plt.close(fig)


def draw_time_plot(filter_column, value_list, df, df_number, ax):
    title_part = {
        'p_random': 'Parametr p_random',
        'alpha': 'Parametr alpha',
        'beta': 'Parametr beta',
        'iterations': 'Liczba iteracji',
        'rho': 'Parametr rho',
        'col_size': 'Rozmiar kolonii',
    }
    df['time'] = pd.to_numeric(df['time'], errors='coerce')
    problem_size = len(df_number)
    main_df = df[df['count'] == str(problem_size)]
    main_df = main_df[main_df['beta'].isin(['1', '3', '6'])]
    mean_times = []
    for val in value_list:
        filtered_df = main_df[main_df[filter_column] == val]
        mean_times.append(filtered_df['time'].mean())

    bars = ax.bar(value_list, mean_times, color='skyblue',
                  edgecolor='black')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.01,
                f'{height:.2f}',
                ha='center', va='bottom', fontsize=10)

    ax.set_xlabel('Wartość')
    ax.set_ylabel('Średni czas wykonania [s]')

    ax.set_title(f'{title_part[filter_column]}', fontsize=14)

    ax.grid(axis='y', linestyle='--', alpha=0.7)


df, df32, df80 = extract_data()

os.makedirs('plots', exist_ok=True)

for d_f in [df32, df80]:
    fig, axes = plt.subplots(3, 2, figsize=(12, 16))
    axes_flat = axes.flatten()
    name = 'A-n32-k5' if len(d_f) == 32 else 'A-n80-k10'
    fig.suptitle(f'Wpływ parametrów na czas wykonywania '
                 f'algorytmu ACO dla pliku {name}.txt', fontsize=16)
    draw_time_plot('rho', ['0.1', '0.3', '0.7'], df, d_f,
                   axes_flat[0])
    draw_time_plot('alpha', ['0.5', '2', '5'], df, d_f,
                   axes_flat[1])
    draw_time_plot('beta', ['1', '3', '6'], df, d_f,
                   axes_flat[2])
    draw_time_plot('col_size', ['15', '40', '80'], df, d_f,
                   axes_flat[3])
    draw_time_plot('p_random', ['0.01', '0.05', '0.1'], df, d_f,
                   axes_flat[4])
    draw_time_plot('iterations', ['100', '300', '600'], df, d_f,
                   axes_flat[5])

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.savefig(f'plots/time-{name}', dpi=300, bbox_inches="tight")
    plt.close()


# draw_comparison_plot('alpha', ['0.5', '5'], df, df32)
draw_comparison_plot('alpha', ['0.5'], df, df80)











