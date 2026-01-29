import ast
import os
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from file import read_solomon_data

all_parameter_list = {
    'file': ['C101', 'R101', 'RC101'],
    'cp': ['0.6', '0.8', '1.0'],
    'mp': ['0.01', '0.1', '0.3', '0.7'],
    'pop': ['20', '60', '150'],
    'sel': ['tournament', 'ranking'],
    'cross': ['single', 'double'],
    'sel_cross': [f"{s}-{c}" for s in ['tournament', 'ranking']
                  for c in ['single', 'double']]
}

reference = {
    'C101': {
        'route': [
            [0, 81, 78, 76, 71, 70, 73, 77, 79, 80, 0],
            [0, 57, 55, 54, 53, 56, 58, 60, 59, 0],
            [0, 98, 96, 95, 94, 92, 93, 97, 100, 99, 0],
            [0, 32, 33, 31, 35, 37, 38, 39, 36, 34, 0],
            [0, 13, 17, 18, 19, 15, 16, 14, 12, 0],
            [0, 90, 87, 86, 83, 82, 84, 85, 88, 89, 91, 0],
            [0, 43, 42, 41, 40, 44, 46, 45, 48, 51, 50, 52, 49, 47, 0],
            [0, 67, 65, 63, 62, 74, 72, 61, 64, 68, 66, 69, 0],
            [0, 5, 3, 7, 8, 10, 11, 9, 6, 4, 2, 1, 75, 0],
            [0, 20, 24, 25, 27, 29, 30, 28, 26, 23, 22, 21, 0]
        ],
        'distance': 828.94
    },
    'R101': {
        'route': [
            [0, 2, 21, 73, 41, 56, 4, 0],
            [0, 5, 83, 61, 85, 37, 93, 0],
            [0, 14, 44, 38, 43, 13, 0],
            [0, 27, 69, 76, 79, 3, 54, 24, 80, 0],
            [0, 28, 12, 40, 53, 26, 0],
            [0, 30, 51, 9, 66, 1, 0],
            [0, 31, 88, 7, 10, 0],
            [0, 33, 29, 78, 34, 35, 77, 0],
            [0, 36, 47, 19, 8, 46, 17, 0],
            [0, 39, 23, 67, 55, 25, 0],
            [0, 45, 82, 18, 84, 60, 89, 0],
            [0, 52, 6, 0],
            [0, 59, 99, 94, 96, 0],
            [0, 62, 11, 90, 20, 32, 70, 0],
            [0, 63, 64, 49, 48, 0],
            [0, 65, 71, 81, 50, 68, 0],
            [0, 72, 75, 22, 74, 58, 0],
            [0, 92, 42, 15, 87, 57, 97, 0],
            [0, 95, 98, 16, 86, 91, 100, 0]
        ],
        'distance': 1650.80
    },
    'RC101': {
        'route': [
            [0, 5, 45, 2, 7, 6, 8, 3, 1, 70, 100, 0],
            [0, 14, 47, 12, 73, 79, 46, 4, 60, 0],
            [0, 27, 29, 31, 30, 34, 26, 32, 93, 0],
            [0, 28, 33, 85, 89, 91, 0],
            [0, 39, 42, 44, 61, 81, 54, 96, 0],
            [0, 59, 75, 87, 97, 58, 77, 0],
            [0, 63, 76, 51, 22, 49, 20, 24, 0],
            [0, 64, 90, 84, 56, 66, 0],
            [0, 65, 52, 99, 57, 86, 74, 0],
            [0, 69, 98, 88, 53, 78, 55, 68, 0],
            [0, 72, 36, 38, 41, 40, 43, 37, 35, 0],
            [0, 82, 11, 15, 16, 9, 10, 13, 17, 0],
            [0, 83, 23, 21, 19, 18, 48, 25, 0],
            [0, 92, 95, 62, 67, 71, 94, 50, 80, 0]
        ],
        'distance': 1696.95
    }
}


def extract_data_from_file_name(file_name: str) -> dict:
    file_data = pd.read_csv(f'wyniki_vrptw/{file_name}')
    file_name = (file_name.replace('.csv', ''))
    name_parts = file_name.split('-')
    name_parts.pop()
    return {
        'file': name_parts[0],
        'pop': name_parts[1],
        'iter': name_parts[2],
        'cp': name_parts[3],
        'cross': name_parts[4],
        'mp': name_parts[5],
        'sel': name_parts[6],
        'best': file_data['best'],
        'best_count': file_data['best_count'],
        'worst': file_data['worst'],
        'worst_count': file_data['worst_count'],
        'avg': file_data['avg'],
        'avg_count': file_data['avg_count'],
        'std': file_data['std'],
        'std_count': file_data['std_count'],
        'time': file_data.iloc[0, -2],
        'routes': file_data['routes'],
        'sel_cross': f"{name_parts[6]}-{name_parts[4]}",
        'shortest_route': file_data['best'].iloc[-1]
    }


def extract_data(before_deadline: bool = True):
    result_folder = "wyniki_vrptw/"
    data_list = []
    deadline = datetime(2026, 1, 29, 12, 0)
    for file in os.listdir(result_folder):
        if not file.endswith(".csv"):
            continue

        file_path = os.path.join(result_folder, file)
        mtime = os.path.getmtime(file_path)
        file_date = datetime.fromtimestamp(mtime)
        if before_deadline:
            should_include = file_date < deadline
        else:
            should_include = file_date >= deadline
        if should_include:
            data = extract_data_from_file_name(file)
            data["filename"] = file
            data_list.append(data)
    all_data = pd.DataFrame(data_list)
    return all_data


def draw_single_plot(ax, df, col, title, val):
    series_list = [row[col] for _, row in df.iterrows()]
    all_data = pd.concat(series_list, axis=1)
    avg = all_data.mean(axis=1)
    ax.plot(avg.values, label=val)
    ax.set_xlabel("Iteracja")
    ax.set_title(title)
    ax.set_ylabel("Wartość")
    ax.legend()


def draw_plot(df, filter_column, value_list):
    params = {
        'best': 'Najkrótsze długości tras',
        'best_count': 'Najmniejsza ilość pojazdów',
        'worst': 'Najdłuższe długości tras',
        'worst_count': 'Największa ilość pojazdów',
        'avg': 'Średnie długości tras',
        'avg_count': 'Średnia ilość pojazdów',
        'std': 'Odchylenia standardowe długości tras',
        'std_count': 'Odchylenia standardowe ilości pojazdów'
    }

    title_part = {
        'cp': 'prawdopodobieństwa krzyżowania',
        'mp': 'prawdopodobieństwa mutacji',
        'pop': 'rozmiaru populacji',
        'sel_cross': 'kombinacji selekcja + krzyżowanie',
    }
    files = all_parameter_list['file']
    for file in files:
        fig, axes = plt.subplots(4, 2, figsize=(12, 17))
        axes_flat = axes.flatten()

        title = (f"Wpływ {title_part[filter_column]} "
                 f"na wyniki VRPTW - {file}")

        fig.suptitle(title, fontsize=16)
        f_filter = df[df['file'] == file]
        for i, (col, title) in enumerate(params.items()):
            ax = axes_flat[i]
            for val in value_list:
                filtered = f_filter[f_filter[filter_column] == val]
                series_list = [row[col] for _, row
                               in filtered.iterrows()]
                if series_list:
                    all_data = pd.concat(series_list, axis=1)
                    avg = all_data.mean(axis=1)
                    ax.plot(avg.values, label=f"{filter_column}={val}")
                ax.set_title(title, fontsize=12, color='darkblue')
                ax.set_xlabel("Iteracja")
                ax.set_ylabel("Wartość")
                ax.legend(fontsize='x-small')

        plt.tight_layout(rect=[0, 0, 1, 0.98])
        save_name = f"plots/vrptw_{filter_column}_f{file}.png"
        plt.savefig(save_name, dpi=300, bbox_inches="tight")
        plt.close()


def draw_time_subplot(ax, df, filter_column, value_list, title):
    df.loc[:, 'time'] = pd.to_numeric(df['time'], errors='coerce')
    mean_times = []
    for val in value_list:
        filtered = df[df[filter_column] == val]
        mean_times.append(filtered['time'].mean())
    ax.bar(value_list, mean_times, color='skyblue', edgecolor='black')
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.set_ylabel('Średni czas [s]')
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    if filter_column == 'sel_cross':
        ax.tick_params(axis='x', rotation=15)


def draw_time_plot(df):
    titles = {
        'cp': 'Prawdopodobieństwo krzyżowania',
        'mp': 'Prawdopodobieństwo mutacji',
        'pop': 'Rozmiar populacji',
        'sel_cross': 'Kombinacja: selekcja + krzyżowanie'
    }
    files = all_parameter_list['file']
    for file in files:
        f_filter = df[df['file'] == file]
        fig, axes = plt.subplots(2, 2, figsize=(12, 16))
        ax_flat = axes.flatten()
        fig.suptitle('Analizu wpływu parametrów '
                     f'na czas wykonania VRPTW - {file}', fontsize=18)
        idx = 0
        for col, values in all_parameter_list.items():
            if col in ['file', 'sel', 'cross']:
                continue
            ax = ax_flat[idx]
            title = f"{titles[col]}"
            draw_time_subplot(ax, f_filter, col, values, title)
            idx += 1
        plt.tight_layout(rect=[0, 0, 1, 0.98])
        plt.savefig(f'plots/vrptw_time_{file}.png', dpi=300)
        plt.close()


def plot_all_paths(ax, data, routes, row_info, distance, number=None):
    depot = data['customers'][0]
    ax.scatter(depot['x'], depot['y'], c='red', marker='s', s=100,
               label='Baza', zorder=5)

    cust_x = [c['x'] for id, c in data['customers'].items() if id != 0]
    cust_y = [c['y'] for id, c in data['customers'].items() if id != 0]
    ax.scatter(cust_x, cust_y, c='blue', marker='o', s=30, alpha=0.6,
               label='Klienci')

    cmap = plt.get_cmap('tab20')

    for i, route in enumerate(routes):
        color = cmap(i % 20)

        route_x = [data['customers'][node]['x'] for node in route]
        route_y = [data['customers'][node]['y'] for node in route]

        ax.plot(route_x, route_y, color=color,
                linewidth=2, alpha=0.8)
    if number:
        info = (
            f"Parametry: Populacja={row_info['pop']}, CP="
            f"{row_info['cp']}, MP={row_info['mp']}, selekcja="
            f"{row_info['sel']}, cross={row_info['cross']}, "
            f"iter={2000 if number == 1 else 3000}"
        )
        ax.annotate(
            info,
            xy=(0.05, 0.05),
            xycoords='axes fraction',
            fontsize=9,
            verticalalignment='bottom',
            bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.7,
                      ec='gray')
        )
        ax.set_title(
            f"Najlepsza trasa z eksperymentu {number}\n"
            f"({len(routes)} pojazdów, długość trasy - {distance:.2f})")
    else:
        ax.set_title(
            f"Najlepsza trasa ze źródła\n"
            f"({len(routes)} pojazdów, długość trasy - {distance:.2f})")
    ax.grid(True, linestyle='--', alpha=0.5)


def get_routes_and_best_row(df, file):
    df_filter = df[df['file'] == file]
    target_index = df_filter.sort_values(by='shortest_route').index[0]
    best = df_filter.loc[target_index]
    return ([ast.literal_eval(r)
             for r in best['routes'].dropna().tolist()], best)


def plot_best_path(df, df2):
    for file in all_parameter_list['file']:
        solomon_data = read_solomon_data(f'solomon-100/In/'
                                         f'{file.lower()}.txt')
        reference_data = reference[file]
        routes_1, best_1 = get_routes_and_best_row(df, file)
        routes_2, best_2 = get_routes_and_best_row(df2, file)

        distance_1 = best_1['shortest_route']
        distance_2 = best_2['shortest_route']
        reference_distance = reference_data['distance']
        fig, axes = plt.subplots(3, 1, figsize=(12, 16))
        plot_all_paths(axes[0], solomon_data, routes_1, best_1,
                       distance_1, 1)
        plot_all_paths(axes[1], solomon_data, routes_2, best_2,
                       distance_2, 2)
        plot_all_paths(axes[2], solomon_data, reference_data[
            'route'], None, reference_distance)
        fig.suptitle(f"Porównanie tras VRPTW - Instancja {file}",
                     fontsize=18)
        plt.tight_layout(rect=[0, 0, 1, 0.98])

        plt.savefig(f'plots/vrptw_route_{file}.png', dpi=300)
        plt.close()

        print(f"\nINSTANCJA {file}\nEksperyment 1."
              f" Najkrótszy dystans - {distance_1:.2f} lista tras:")
        for route in routes_1:
            print(route)
        print(f"\nEksperyment 2. "
              f"Najkrótszy dystans - {distance_2:.2f} lista tras:")
        for route in routes_2:
            print(route)
        print(f"Lista najlepszych trasy ze źródła"
              f" - dystans {reference_distance:.2f}:")
        for route in reference_data['route']:
            print(route)


first_experiment_data = extract_data(before_deadline=True)
second_experiment_data = extract_data(before_deadline=False)

plot_best_path(first_experiment_data, second_experiment_data)

os.makedirs('plots', exist_ok=True)
draw_time_plot(first_experiment_data)

for key, value in all_parameter_list.items():
    if key in ['file', 'sel', 'cross']:
        continue
    draw_plot(first_experiment_data, key, value)
