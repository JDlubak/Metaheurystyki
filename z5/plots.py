import os

import matplotlib.pyplot as plt
import pandas as pd

all_parameter_list = {
    'czastki': ['10', '30', '80'],
    'iter': ['500', '200', '100'],
    'iner': ['0.2', '0.5', '0.8'],
    'stala_poznawcza': ['0.3', '1.2', '2.0'],
    'stala_spoleczna': ['0.3', '1.2', '2.0']
}


def extract_data_from_file_name(file_name: str) -> dict:
    file_data = pd.read_csv(f'wyniki_PSO/{file_name}')
    file_name = (file_name.replace('.csv', ''))
    name_parts = file_name.split('-')
    name_parts.pop()
    return {
        'func': name_parts[0],
        'czastki': name_parts[1],
        'iter': name_parts[2],
        'iner': name_parts[3],
        'stala_poznawcza': name_parts[4],
        'stala_spoleczna': name_parts[5],
        'best': file_data['najlepsze'],
        'worst': file_data['najgorsze'],
        'avg': file_data['srednie'],
        'std': file_data['odchylenia'],
        'median': file_data['kwantyl_50'],
        'q25': file_data['kwantyl_25'],
        'q75': file_data['kwantyl_75'],
        'q90': file_data['kwantyl_90'],
        'time': file_data.iloc[0, -1],
    }


def extract_data():
    result_folder = "wyniki_PSO/"
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


def draw_plot(df, filter_column, value_list, use_log_scale=False):
    comparison_params = {
        'best': 'Najlepsze wartości w kolejnych iteracjach',
        'worst': 'Najgorsze wartości w kolejnych iteracjach',
        'avg': 'Średnie wartości w kolejnych iteracjach',
        'median': 'Mediana w kolejnych iteracjach',
        'std': 'Odchylenia standardowe w kolejnych iteracjach'
    }

    quantile_params = {
        'worst': 'Najgorszy wynik',
        'q90': 'Kwantyl 90',
        'q75': '3 kwartyl',
        'median': 'Mediana',
        'q25': '1 kwartyl',
        'best': 'Najlepszy wynik'
    }

    title_part = {
        'czastki': 'liczby cząstek',
        'iter': 'liczby iteracji',
        'iner': 'współczynnika inercji',
        'stala_poznawcza': 'stałej poznawczej',
        'stala_spoleczna': 'stałej społecznej',
    }

    for function in (['1', '2']):
        fig, axes = plt.subplots(4, 2, figsize=(10, 16))
        axes_flat = axes.flatten()
        title_end = "funkcja Beale’a" if function == '1' \
            else 'funkcja Himmelblaua'
        log_add = " (skala logarytmiczna)" if use_log_scale else ""
        title = (f"Wpływ {title_part[filter_column]} "
                 f"na wyniki algorytmu PSO - {title_end}{log_add}")

        fig.suptitle(title, fontsize=16)
        f_filter = df[df['func'] == function]
        for i, (col, title) in enumerate(comparison_params.items()):
            ax = axes_flat[i]
            if use_log_scale:
                ax.set_yscale('log')
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

        for j, val in enumerate(value_list):
            ax = axes_flat[5 + j]
            if use_log_scale:
                ax.set_yscale('log')
            filtered = f_filter[f_filter[filter_column] == val]
            q25_series = [row['q25'] for _, row in filtered.iterrows()]
            q75_series = [row['q75'] for _, row in filtered.iterrows()]
            if q25_series and q75_series:
                q25_avg = pd.concat(q25_series, axis=1).mean(axis=1)
                q75_avg = pd.concat(q75_series, axis=1).mean(axis=1)

                ax.fill_between(range(len(q25_avg)), q25_avg.values,
                                q75_avg.values,
                                color='gray', alpha=0.3)

            for param, label in quantile_params.items():
                series_list = [row[param] for _, row in
                               filtered.iterrows()]
                if series_list:
                    all_data = pd.concat(series_list, axis=1)
                    avg = all_data.mean(axis=1)
                    lw = 2 if param == 'median' else 1
                    ax.plot(avg.values, label=label, linewidth=lw)

            word = 'równego' if filter_column == 'iner' else \
                'równej'
            ax.set_title(f'Rozkład cząstek dla '
                         f'{title_part[filter_column]} {word}'
                         f' {val}',
                         fontsize=12,
                         color='darkblue')
            ax.set_xlabel("Iteracja")
            ax.set_ylabel("Wartość")
            ax.legend(fontsize='xx-small', loc='upper right', ncol=2)

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        save_name = (f"plots/pso_{filter_column}_f{function}"
                     f"{"-log" if use_log_scale else ""}.png")
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


def draw_time_plot(df):
    titles = {
        'czastki': 'Liczba cząstek',
        'iter': 'Liczba iteracji',
        'iner': 'Współczynnik inercji',
        'stala_poznawcza': 'Stała poznawcza',
        'stala_spoleczna': 'Stała społeczna'
    }
    y_limits = {
        'czastki': 0.07,
        'iter': 0.1,
        'iner': 0.05,
        'stala_poznawcza': 0.05,
        'stala_spoleczna': 0.05
    }
    fig, axes = plt.subplots(5, 2, figsize=(12, 22))
    fig.suptitle('Analizu wpływu parametrów na czas wykonania PSO',
                 fontsize=18)
    for row_idx, (col, values) in enumerate(all_parameter_list.items()):
        for col_idx, function in enumerate(['1', '2']):
            ax = axes[row_idx, col_idx]
            f_filter = df[df['func'] == function]
            func_title = "Beale" if function == '1' else "Himmelblau"
            title = f"{titles[col]} ({func_title})"
            draw_time_subplot(ax, f_filter, col, values, title)
            limit = y_limits.get(col, 0.05)
            ax.set_ylim(0, limit)
    plt.tight_layout(rect=[0, 0, 1, 0.98])
    plt.savefig(f'plots/pso_time.png', dpi=300)
    plt.close()


data = extract_data()
os.makedirs('plots', exist_ok=True)
draw_time_plot(data)

for key, value in all_parameter_list.items():
    draw_plot(data, key, value, use_log_scale=True)
    draw_plot(data, key, value, use_log_scale=False)



