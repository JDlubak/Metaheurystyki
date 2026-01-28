import os

import matplotlib.pyplot as plt
import pandas as pd

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
    }


def extract_data():
    result_folder = "wyniki_vrptw/"
    data_list = []
    for file in os.listdir(result_folder):
        if not file.endswith(".csv"):
            continue
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
        fig, axes = plt.subplots(4, 2, figsize=(12, 20))
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


data = extract_data()
os.makedirs('plots', exist_ok=True)
draw_time_plot(data)

for key, value in all_parameter_list.items():
    if key in ['file', 'sel', 'cross']:
        continue
    draw_plot(data, key, value)
