import os
import sys
import argparse
import pandas as pd
import scanpy as sc
import PyComplexHeatmap


def parse_args():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Plotting")
    parser.add_argument("-t", "--type", required=True, help="Type of plot (e.g., line, bar, scatter, hist)")
    parser.add_argument("-f", "--file", help="Path to the data file (csv, xlsx, xls format)")
    parser.add_argument("-o", "--output", help="Output directory path")
    parser.add_argument("--preview", default=False, type=bool, help="Preview")
    parser.add_argument("--color", nargs='+', help="Custom colors for the heatmap (e.g., --color blue cyan yellow red)")
    parser.add_argument("--linestyle", help="Line style for line plot")
    parser.add_argument("--marker", help="Marker style for scatter plot")
    parser.add_argument("--bins", type=int, help="Number of bins for histogram")
    parser.add_argument("--regression", action="store_true", help="Whether or not to do regression plot")
    parser.add_argument("--annotate", action="store_true", help="annotate plot")
    parser.add_argument('--gene-list', type=str, help='输入基因列表文件，每行一个基因')
    parser.add_argument('--species', type=str, choices=['human', 'mouse'], default="mouse",
                        help='choice for species (only human and mouse)')
    parser.add_argument('--analysis-type', type=str, choices=['go', 'kegg'], help='analysis type')
    parser.add_argument('--top-n', type=int, default=20, help='top n results')

    return parser.parse_args()


def get_file_type(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower()


def load_data_from_file(file_path):
    # 如果文件路径为 None，返回默认数据
    if file_path is None:
        raise FileNotFoundError("File path cannot be None")

    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise FileExistsError(f"File is not exists: {file_path}")

    if not os.path.isfile(file_path):
        raise Exception(f"Path is exists，but not a file type: {file_path}")

    # 获取文件扩展名
    file_extension = get_file_type(file_path)

    # 检查文件类型是否允许
    allowed_file_types = ['.xls', '.xlsx', '.csv', '.txt']
    if file_extension not in allowed_file_types:
        raise ValueError("The type of the file is not allowed, only .xls, .xlsx, .csv, .txt, .h5ad files are allowed")

    # 根据文件扩展名加载数据
    if file_extension == '.csv':
        return pd.read_csv(file_path), file_extension
    elif file_extension == ".xlsx":
        try:
            # 尝试读取 Excel 文件
            data = pd.read_excel(file_path), file_extension
            return data
        except FileNotFoundError:
            print(f"Error: File not found at path {file_path}")
            return None
        except ValueError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
    elif file_extension == ".xls":
        return pd.read_excel(file_path, engine='xlrd'), file_extension
    elif file_extension == '.txt':
        # 尝试自动检测分隔符
        try:
            return pd.read_csv(file_path, sep=None, engine='python'), file_extension
        except Exception as e:
            print(f"Error reading TXT file: {e}")
            sys.exit(1)
    elif file_extension == ".h5ad":
        try:
            return sc.read_h5ad(file_path), file_extension
        except Exception as e:
            print(f"Error reading h5ad file: {e}")
            sys.exit(1)
    else:
        print(f"Unsupported file format: {file_extension}")
        sys.exit(1)
