def extract_data_from_file_name(file_name: str) -> dict:
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
    }


data = extract_data_from_file_name('results-double-ranking-200-300-0.81-0.1.csv-1')
print(data)
