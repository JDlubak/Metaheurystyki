import matplotlib.pyplot as plt
import pandas as pd
import os
from read_result import extract_data_from_file_name

result_folder = "results/"

data_list = []

for file in os.listdir(result_folder):
    if not file.endswith(".csv"):
        continue

    data = extract_data_from_file_name(file)
    data["filename"] = file
    data_list.append(data)

df = pd.DataFrame(data_list)


def getName(data):
    return f"{data['sel']}, {data['cross']}"


def getName(data):
    return f"{data['sel']}, {data['cross']}"

def draw_plots(iter_val, pop_val, cp_val, mp_val):
    filtered_df = df[
        (df['iter'] == str(iter_val)) &
        (df['pop'] == str(pop_val)) &
        (df['cp'] == str(cp_val)) &
        (df['mp'] == str(mp_val))
    ]

    if filtered_df.empty:
        print("Brak danych dla podanych parametrów.")
        return

    configurations_df = filtered_df[['sel', 'cross']].drop_duplicates()

    comparison_avg = {}
    comparison_best = {}
    comparison_worst = {}

    def plot_series(series_list, mean_series, title):
        plt.figure(figsize=(14, 6))
        for col in series_list.columns:
            plt.plot(series_list[col], '--', linewidth=1, label=col)
        plt.plot(mean_series, linewidth=3, color='black', label='Średnia')
        plt.title(title)
        plt.xlabel('Liczba iteracji')
        plt.ylabel('Wartość PLN')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    for _, config_row in configurations_df.iterrows():
        sel_val = config_row['sel']
        cross_val = config_row['cross']
        config_name = getName(config_row)

        matching = filtered_df[
            (filtered_df['sel'] == sel_val) &
            (filtered_df['cross'] == cross_val)
        ]

        all_avgs_list = [row['avg'].rename(f"Uruchomienie {i+1}") for i, (_, row) in enumerate(matching.iterrows())]
        all_best_list = [row['best'].rename(f"Uruchomienie {i+1}") for i, (_, row) in enumerate(matching.iterrows())]
        all_worst_list = [row['worst'].rename(f"Uruchomienie {i+1}") for i, (_, row) in enumerate(matching.iterrows())]

        # --- AVG ---
        if all_avgs_list:
            all_avgs = pd.concat(all_avgs_list, axis=1)
            mean_avg = all_avgs.mean(axis=1)
            comparison_avg[config_name] = mean_avg
            plot_series(all_avgs, mean_avg, f"Średnia wartość – {config_name}")

        # --- BEST ---
        if all_best_list:
            all_best = pd.concat(all_best_list, axis=1)
            mean_best = all_best.mean(axis=1)
            comparison_best[config_name] = mean_best
            plot_series(all_best, mean_best, f"Najlepsza wartość – {config_name}")

        # --- WORST ---
        if all_worst_list:
            all_worst = pd.concat(all_worst_list, axis=1)
            mean_worst = all_worst.mean(axis=1)
            comparison_worst[config_name] = mean_worst
            plot_series(all_worst, mean_worst, f"Najgorsza wartość – {config_name}")


def draw_comparison_plot(filter_column, value_list):
    comparison_avg = {}
    comparison_best = {}
    comparison_worst = {}

    title_part = {
        'cp': 'prawdopodobieństwa krzyżowania',
        'mp': 'prawdopodobieństwa mutacji',
        'iter': 'liczby iteracji',
        'pop': 'liczby populacji'
    }

    for val in value_list:
        filtered_df = df[df[filter_column] == val]

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
        plt.title(f'Średnie rozwiązania w zależności od {title_part[filter_column]}')
        plt.xlabel('Liczba iteracji')
        plt.ylabel('Wartość PLN')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    if comparison_best:
        plt.figure(figsize=(14, 6))
        for name, series in comparison_best.items():
            plt.plot(series, linewidth=2, label=name)
        plt.title(f'Najlepsze rozwiązania w zależności od {title_part[filter_column]}')
        plt.xlabel('Liczba iteracji')
        plt.ylabel('Wartość PLN')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    if comparison_worst:
        plt.figure(figsize=(14, 6))
        for name, series in comparison_worst.items():
            plt.plot(series, linewidth=2, label=name)
        plt.title(f'Najgorsze rozwiązania w zależności od {title_part[filter_column]}')
        plt.xlabel('Liczba iteracji')
        plt.ylabel('Wartość PLN')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()


def draw_comparison_plots(col1='cross', col2='sel'):
    comparison_avg = {}
    comparison_best = {}
    comparison_worst = {}

    title_part = {
        'cross': 'metody krzyżowania',
        'sel': 'metody selekcji'
    }

    # Grupowanie po dwóch kolumnach
    grouped = df.groupby([col1, col2])

    for (val1, val2), group in grouped:
        label = f"{val1}, {val2}"

        # Średnie po uruchomieniach
        all_avgs_list = [row['avg'] for _, row in group.iterrows()]
        all_best_list = [row['best'] for _, row in group.iterrows()]
        all_worst_list = [row['worst'] for _, row in group.iterrows()]

        if all_avgs_list:
            comparison_avg[label] = pd.concat(all_avgs_list, axis=1).mean(axis=1)
        if all_best_list:
            comparison_best[label] = pd.concat(all_best_list, axis=1).mean(axis=1)
        if all_worst_list:
            comparison_worst[label] = pd.concat(all_worst_list, axis=1).mean(axis=1)

    # Wykresy
    for name, comp_dict, title_suffix in [
        ("Średnie", comparison_avg, "Średnie rozwiązania"),
        ("Najlepsze", comparison_best, "Najlepsze rozwiązania"),
        ("Najgorsze", comparison_worst, "Najgorsze rozwiązania")
    ]:
        if comp_dict:
            plt.figure(figsize=(14, 6))
            for label, series in comp_dict.items():
                plt.plot(series, linewidth=2, label=label)
            plt.title(f"{title_suffix} w zależności od {title_part[col1]} i {title_part[col2]}")
            plt.xlabel("Liczba iteracji")
            plt.ylabel("Wartość PLN")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            plt.show()


draw_comparison_plots()
draw_comparison_plot('cp', ['0.6', '0.8', '1.0'])
draw_comparison_plot('mp', ['0.01', '0.05', '0.1'])
draw_comparison_plot('pop', ['50', '100', '200'])
draw_comparison_plot('iter', ['1000', '500', '200'])
draw_plots(500, 100, 0.8, 0.05)
