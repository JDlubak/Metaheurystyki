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

def draw_plots(iter_val, pop_val, cp_val, mp_val):
    filtered_df = df[
        (df['iter'] == str(iter_val)) &
        (df['pop'] == str(pop_val)) &
        (df['cp'] == str(cp_val)) &
        (df['mp'] == str(mp_val))
    ]

    # unikamy apply() i DeprecationWarning
    configurations_df = filtered_df[['sel', 'cross']].drop_duplicates()
    configurations = [getName(row) for _, row in configurations_df.iterrows()]

    comparison_avg = {}
    comparison_best = {}

    for config_name in configurations:
        matching = filtered_df[filtered_df.apply(lambda row: getName(row) == config_name, axis=1)]

        all_avgs_list = []
        all_best_list = []

        for i, (_, row) in enumerate(matching.iterrows(), start=1):
            all_avgs_list.append(row['avg'].rename(f"Uruchomienie {i}"))
            all_best_list.append(row['best'].rename(f"Uruchomienie {i}"))

        # --- AVG ---
        if all_avgs_list:
            all_avgs = pd.concat(all_avgs_list, axis=1)
            mean_avg = all_avgs.mean(axis=1)
            comparison_avg[config_name] = mean_avg

            plt.figure(figsize=(14, 6))
            for col in all_avgs.columns:
                plt.plot(all_avgs[col], '--', linewidth=1, label=col)
            plt.plot(mean_avg, linewidth=3, color='black', label='Średnia')
            plt.title(f"AVG – {config_name}")
            plt.xlabel('Iteracja')
            plt.ylabel('Wartość PLN')
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            plt.show()

        # --- BEST ---
        if all_best_list:
            all_best = pd.concat(all_best_list, axis=1)
            mean_best = all_best.mean(axis=1)
            comparison_best[config_name] = mean_best

            plt.figure(figsize=(14, 6))
            for col in all_best.columns:
                plt.plot(all_best[col], '--', linewidth=1, label=col)
            plt.plot(mean_best, linewidth=3, color='black', label='Średnia')
            plt.title(f"BEST – {config_name}")
            plt.xlabel('Iteracja')
            plt.ylabel('Wartość PLN')
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            plt.show()

    # --- PORÓWNANIE AVG ---
    if comparison_avg:
        plt.figure(figsize=(14, 6))
        for name, series in comparison_avg.items():
            plt.plot(series, linewidth=2, label=name)
        plt.title('PORÓWNANIE: Średnich rozwiązań')
        plt.xlabel('Iteracja')
        plt.ylabel('Wartość PLN')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    # --- PORÓWNANIE BEST ---
    if comparison_best:
        plt.figure(figsize=(14, 6))
        for name, series in comparison_best.items():
            plt.plot(series, linewidth=2, label=name)
        plt.title('PORÓWNANIE: Średnich najlepszych rozwiązań')
        plt.xlabel('Iteracja')
        plt.ylabel('Wartość PLN')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

draw_plots(500, 200, 0.8, 0.1)