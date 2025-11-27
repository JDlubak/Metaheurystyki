import matplotlib.pyplot as plt
import pandas as pd

result_folder = "results/"

configurations = [
    f'{result_folder}results-single-ranking-500-200-0.8-0.05-',
    f'{result_folder}results-single-roulette-500-200-0.8-0.05-',
    f'{result_folder}results-double-ranking-500-200-0.8-0.05-',
    f'{result_folder}results-double-roulette-500-200-0.8-0.05-'
]

def getName(name):
    if "ranking" in name:
        base = "Ranking"
    else:
        base = "Ruletka"

    if "single" in name:
        return base + "-single"
    else:
        return base + "-double"

comparison_avg = {}
comparison_best = {}

for config_name in configurations:
    # --- AVG ---
    all_avgs_list = []
    for i in range(1, 6):
        filename = f"{config_name}{i}.csv"
        try:
            df = pd.read_csv(filename)
            all_avgs_list.append(df['Avg'].rename(f'Uruchomienie{i}'))
        except FileNotFoundError:
            print(f"Brak pliku: {filename}")

    if all_avgs_list:
        all_avgs = pd.concat(all_avgs_list, axis=1)
        mean_avg_series = all_avgs.mean(axis=1)
        comparison_avg[config_name] = mean_avg_series

        plt.figure(figsize=(14, 6))
        for col in all_avgs.columns:
            plt.plot(all_avgs.index, all_avgs[col], '--', linewidth=1, label=col)

        plt.plot(mean_avg_series.index, mean_avg_series, linewidth=3, color='black', label='Średnia')

        plt.title(getName(config_name))
        plt.xlabel('Iteracja')
        plt.ylabel('Wartosc w PLN')
        plt.xticks(range(0, 500, 50))
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # --- BEST ---
    all_best_list = []
    for i in range(1,6):
        filename = f"{config_name}{i}.csv"
        try:
            df = pd.read_csv(filename)
            all_best_list.append(df['Best_Value'].rename(f'Uruchomienie{i}'))
        except FileNotFoundError:
            print(f"Brak pliku: {filename}")

    if all_best_list:
        all_best = pd.concat(all_best_list, axis=1)
        mean_best_series = all_best.mean(axis=1)
        comparison_best[config_name] = mean_best_series

        plt.figure(figsize=(14, 6))
        for col in all_best.columns:
            plt.plot(all_best.index, all_best[col], '--', linewidth=1, label=col)

        plt.plot(mean_best_series.index, mean_best_series, linewidth=3, color='black', label='Średnia')

        plt.title(getName(config_name))
        plt.xlabel('Iteracja')
        plt.ylabel('Wartosc w PLN')
        plt.xticks(range(0, 500, 50))
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

# --- COMPARISON AVG ---
if comparison_avg:
    plt.figure(figsize=(14, 6))
    for name, series in comparison_avg.items():
        plt.plot(series.index, series, linewidth=2, label=getName(name))

    plt.title('PORÓWNANIE: Średnich rozwiązań')
    plt.xlabel('Iteracja')
    plt.ylabel('Wartosc w PLN')
    plt.xticks(range(0, 500, 50))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# --- COMPARISON BEST ---
if comparison_best:
    plt.figure(figsize=(14, 6))
    for name, series in comparison_best.items():
        plt.plot(series.index, series, linewidth=2, label=getName(name))

    plt.title('PORÓWNANIE: Średnie najlepsze rozwiązania')
    plt.xlabel('Iteracja')
    plt.ylabel('Wartosc w PLN')
    plt.xticks(range(0, 500, 50))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
