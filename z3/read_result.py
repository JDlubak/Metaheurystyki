import pandas as pd
from load_save_operations import load_data


def extract_data_from_file_name(file_name: str) -> dict:
    file_data = pd.read_csv(f'results/{file_name}')
    file_name = file_name.replace('.csv', '').replace('results-', '')
    print(file_name)
    name_parts = file_name.split('-')
    name_parts.pop()
    print(name_parts)
    return {
        'cross': name_parts[0],
        'sel': name_parts[1],
        'iter': name_parts[2],
        'pop': name_parts[3],
        'cp': name_parts[4],
        'mp': name_parts[5],
        'data': file_data.iloc[:, :-1],
        'time': file_data.iloc[0, -1]
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


data = extract_data_from_file_name('results-double-ranking-200-300-0.81-0.1-1.csv')
best_backpack = get_best_backpack(data['data'])
worst_backpack = get_worst_backpack(data['data'])
print(best_backpack)
print(worst_backpack)
print(get_items_from_backpack(best_backpack))
print(get_items_from_backpack(worst_backpack))
