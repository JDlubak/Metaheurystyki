import pandas as pd


def read_file(filename):
    data = pd.read_csv(filepath_or_buffer=filename,
                       sep=r'\s+',
                       header=None,
                       names=["index", "x", "y"])
    data.set_index('index', inplace=True)
    data.index = data.index - 1
    return data
