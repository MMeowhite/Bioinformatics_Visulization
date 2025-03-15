import os
import sys
import argparse
import pandas as pd
import numpy as np


def parse_args():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Plotting Tool")
    parser.add_argument("-t", "--type", required=True, help="Type of plot (e.g., line, bar, scatter, hist)")
    parser.add_argument("-f", "--file", help="Path to the data file (csv, xlsx, xls format)")
    parser.add_argument("-o", "--output", help="Output directory path")
    parser.add_argument("--preview", default=False, type=bool, help="Preview")
    parser.add_argument("--color", nargs='+', help="Custom colors for the heatmap (e.g., --color blue cyan yellow red)")
    parser.add_argument("--linestyle", help="Line style for line plot")
    parser.add_argument("--marker", help="Marker style for scatter plot")
    parser.add_argument("--bins", type=int, help="Number of bins for histogram")
    parser.add_argument("--annotate", action="store_true", help="annotate plot")

    return parser.parse_args()


def get_file_type(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower()


def load_data_from_file(file_path):
    # 如果文件路径为 None，返回默认数据
    if file_path is None:
        return {'x': [1, 2, 3, 4, 5], 'y': [10, 20, 25, 30, 40]}

    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise Exception(f"文件不存在: {file_path}")

    if not os.path.isfile(file_path):
        raise Exception(f"路径存在，但不是一个文件: {file_path}")

    # 获取文件扩展名
    file_extension = get_file_type(file_path)

    # 检查文件类型是否允许
    allowed_file_types = ['.xls', '.xlsx', '.csv', '.txt']
    if file_extension not in allowed_file_types:
        raise Exception("The type of the file is not allowed, only .xls, .xlsx, .csv, .txt files are allowed")

    # 根据文件扩展名加载数据
    if file_extension == '.csv':
        return pd.read_csv(file_path)
    elif file_extension in ['.xls', '.xlsx']:
        return pd.read_excel(file_path)
    elif file_extension == '.txt':
        # 尝试自动检测分隔符
        try:
            return pd.read_csv(file_path, sep=None, engine='python')
        except Exception as e:
            print(f"Error reading TXT file: {e}")
            sys.exit(1)
    else:
        print(f"Unsupported file format: {file_extension}")
        sys.exit(1)
