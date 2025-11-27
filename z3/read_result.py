import pandas as pd
from load_save_operations import load_data


def extract_data_from_file_name(file_name: str) -> dict:
    file_data = pd.read_csv(f'results/{file_name}')
    file_name = file_name.replace('.csv', '').replace('results-', '')
    name_parts = file_name.split('-')
    name_parts.pop()
    return {
        'cross': "k. jednopunktowe" if name_parts[0] == "single" else "k. dwupunktowe",
        'sel': "m. ruletkowa" if name_parts[1] == "roulette" else "m. rankingowa",
        'iter': name_parts[2],
        'pop': name_parts[3],
        'cp': name_parts[4],
        'mp': name_parts[5],
        'avg': file_data["Avg"],
        'best': file_data["Best_Value"],
        'time': file_data.iloc[0, -1],
        'filename': file_name + ".csv"
    }


def get_best_backpack(data: pd.DataFrame) -> str:
    return data.loc[data['Best_Value'].idxmax(), 'Best_Name']


def get_worst_backpack(data: pd.DataFrame) -> str:
    return data.loc[data['Worst_Value'].idxmin(), 'Worst_Name']


def get_items_from_backpack(backpack: str) -> list:
    item_list = load_data()
    print(item_list)
    backpack_list = []
    for i, item in enumerate(backpack, start=1):
        if item == '1':
            backpack_list.append(item_list[i]['Name'])
    return backpack_list

