import matplotlib.pyplot as plt
import os
import pandas as pd


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


def draw_comparison_plot(df, filter_column, value_list):
    os.makedirs('plots', exist_ok=True)
    parameters = {
        'best': 'najlepsze',
        'worst': 'najgorsze',
        'avg': 'srednie',
        'std': 'odchylenia',
        'median': 'kwantyl_50',
        'q25': 'kwantyl_25',
        'q75': 'kwantyl_75',
        'q90': 'kwantyl_90',
    }

    title_part = {
        'czastki': 'liczby cząstek',
        'iter': 'liczby iteracji',
        'iner': 'współczynnika inercji',
        'stala_poznawcza': 'stałej poznawczej',
        'stala_spoleczna': 'stałej społecznej',
    }
    for function in (['1', '2']):
        func_filter = df[df['func'] == function]
        fig, axes = plt.subplots(4, 2, figsize=(12, 16))
        axes_flat = axes.flatten()
        title_end = "funkcja Beale’a" if function == '1' \
            else 'funkcja Himmelblaua'
        fig.suptitle(f'Wpływ {title_part[filter_column]} na wyniki '
                     f'algorytmu PSO - {title_end}')

        for val in value_list:
            filtered = func_filter[func_filter[filter_column] == val]
            for j, (col, title) in enumerate(parameters.items()):
                draw_single_plot(axes_flat[j], filtered, col, title,
                                 val)

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig(f'plots/pso-{filter_column}-'
                    f'{title_end.replace(' ', '_')}',
                    dpi=300, bbox_inches="tight")
        plt.close()


all_parameter_list = {
    'czastki': ['20', '50', '100'],
    'iter': ['200', '100', '50'],
    'iner': ['0.3', '0.5', '0.7'],
    'stala_poznawcza': ['1.0', '1.5', '2.0'],
    'stala_spoleczna': ['0.5', '1.0', '1.5']
}

data = extract_data()
for key, value_list in all_parameter_list.items():
    draw_comparison_plot(data, key, value_list)
