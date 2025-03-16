import pandas as pd
import numpy as np


def data_processing(args, data, **kwargs):
    # 读取 Excel 文件，不将第一行作为列名
    data = pd.read_excel(args.file, header=None)
    rownames = np.array(data.iloc[:, 0].values.tolist()[1:], dtype=str)
    colnames = np.array(data.iloc[0].values.tolist()[1:], dtype=str)
    heat_data = np.array(data.iloc[1:, 1:].values, dtype=float)
    print(f"rownames: {rownames.shape}, colnames: {colnames.shape}")
    print("Heatmap data shape:", heat_data.shape)
    print("Heatmap data type:", heat_data.dtype)
    process_data = {
        'rownames': rownames,
        'colnames': colnames,
        'heat_data': heat_data
    }

    print(f"kwargs: {kwargs}")
    return process_data, kwargs
