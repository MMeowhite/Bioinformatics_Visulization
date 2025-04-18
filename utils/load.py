import os
import sys
import argparse
import pandas as pd
import scanpy as sc
import re


def parse_args():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Quick Bioinformatics Plotting")
    parser.add_argument("-t", "--type", required=True, help="Type of plot (e.g., line, bar, scatter, hist)")
    parser.add_argument("-f", "--file", help="Path to the data file (csv, xlsx, xls format)")
    parser.add_argument("-o", "--output", help="Output directory path")
    parser.add_argument("--preview", default=False, type=bool, help="Preview")
    parser.add_argument("--figsize", help="Figure size in inches")
    parser.add_argument("--layout", type=str, help="the layout of the plotting")
    parser.add_argument("--color", nargs='+', help="Custom colors for the heatmap (e.g., --color blue cyan yellow red)")
    parser.add_argument("--linestyle", help="Line style")
    parser.add_argument("--marker", help="Marker style")
    parser.add_argument("--bins", type=int, help="Number of bins for histogram")
    parser.add_argument("--regression", action="store_true", help="Whether or not to do regression plot")
    parser.add_argument("--annotate", action="store_true", help="annotate plot")
    parser.add_argument('--gene-list', type=str, help='输入基因列表文件，每行一个基因')
    parser.add_argument('--gene-set', type=str, help='input gene sets')
    parser.add_argument('--species', '--organism', type=str, choices=['human', 'mouse'], default="mouse",
                        help='choice for species (only human and mouse)')
    parser.add_argument('--analysis-type', type=str, choices=['go', 'kegg'], help='analysis type')
    parser.add_argument('--top-n', type=int, default=20, help='top n results')

    return parser.parse_args()


def get_file_type(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower()


# def check_files_in_directory(directory_path):
#     # 检查目录是否存在
#     if not os.path.exists(directory_path):
#         print(f"Directory '{directory_path}' does not exist")
#         return False
#
#     # 获取目录中的所有文件
#     files_in_directory = os.listdir(directory_path)
#
#     # 检查必须存在的文件
#     required_files = ['barcodes.tsv', 'matrix.mtx']
#     found_required = {file: False for file in required_files}
#
#     # 检查可选存在的文件（只要存在其中一个即可）
#     optional_files = ['genes.tsv', 'features.tsv']
#     found_optional = False
#
#     for file in files_in_directory:
#         # 检查必须存在的文件
#         for required_file in required_files:
#             if required_file in file:
#                 found_required[required_file] = True
#
#         # 检查可选存在的文件
#         for optional_file in optional_files:
#             if optional_file in file:
#                 found_optional = True
#
#     # 检查必须存在的文件是否都存在
#     for required_file, found in found_required.items():
#         if not found:
#             print(f"File containing '{required_file}' does not exist")
#             return False
#
#     # 检查可选存在的文件是否存在至少一个
#     if not found_optional:
#         print(f"At least one of the files containing 'genes.tsv' or 'features.tsv' must exist")
#         return False
#
#     print("All required files exist")
#     return True


def check_directory_structure(file_path):
    """
    检查目录结构是否符合要求。

    :param file_path: 包含多个组目录的父目录路径。
    :return: 如果所有组都符合要求，返回 True；否则返回 False。
    """
    # 检查父目录是否存在
    if not os.path.exists(file_path):
        print(f"Parent directory '{file_path}' does not exist")
        return False

    # 获取所有子目录
    group_dirs = [os.path.join(file_path, d) for d in os.listdir(file_path) if os.path.isdir(os.path.join(file_path, d))]

    if not group_dirs:
        print(f"No subdirectories found in '{file_path}'")
        return False

    # 检查每个子目录
    for group_dir in group_dirs:
        group_name = os.path.basename(group_dir)
        print(f"Checking group: {group_name}")

        # 检查子目录是否存在
        if not os.path.exists(group_dir):
            print(f"Group directory '{group_dir}' does not exist")
            return False

        # 获取子目录中的所有文件
        files_in_directory = os.listdir(group_dir)

        # 检查必须存在的文件
        required_files = ['barcodes.tsv', 'matrix.mtx.gz']
        found_required = {file: False for file in required_files}

        # 检查可选存在的文件（只要存在其中一个即可）
        optional_files = ['genes.tsv', 'features.tsv']
        found_optional = False

        for file in files_in_directory:
            # 检查必须存在的文件
            for required_file in required_files:
                if required_file in file:
                    found_required[required_file] = True

            # 检查可选存在的文件
            for optional_file in optional_files:
                if optional_file in file:
                    found_optional = True

        # 检查必须存在的文件是否都存在
        for required_file, found in found_required.items():
            if not found:
                print(f"File containing '{required_file}' does not exist in group '{group_name}'")
                return False

        # 检查可选存在的文件是否存在至少一个
        if not found_optional:
            print(f"At least one of the files containing 'genes.tsv' or 'features.tsv' must exist in group '{group_name}'")
            return False

    print("All groups have the required structure")
    return True


def read_and_concatenate_groups(file_path):
    """
    读取多个组的10x Genomics数据并合并。

    :param file_path: 包含多个组目录的父目录路径。
    :return: 合并后的 AnnData 对象。
    """
    # 获取所有组的目录
    group_dirs = [os.path.join(file_path, d) for d in os.listdir(file_path) if os.path.isdir(os.path.join(file_path, d))]

    # 读取每个组的数据
    adatas = []
    for group_dir in group_dirs:
        # 读取10x Genomics数据
        adata = sc.read_10x_mtx(
            path=group_dir,  # 组的目录路径
            var_names="gene_symbols",  # 使用基因符号作为变量名
            cache=True,  # 写入缓存文件以加快后续读取
        )

        # 添加组信息到 obs
        group_name = os.path.basename(group_dir)
        adata.obs['group'] = group_name

        adatas.append(adata)

    # 合并所有组的数据
    if adatas:
        combined_adata = sc.concat(adatas)
        return combined_adata
    else:
        print("No groups found.")
        return None


def load_data_from_file(file_path):
    # 如果文件路径为 None，返回默认数据
    if file_path is None:
        raise FileNotFoundError("File or directory path cannot be None")

    # 检查是否是文件夹
    if not os.path.isfile(file_path):
        # 不是文件，而是一个文件夹
        if check_directory_structure(file_path):
            print("all singe-cell directory have the required structure")

        return read_and_concatenate_groups(file_path), None


        # 检查文件夹中是否含有barcodes.tsv, genes.tsv(features.tsv), matrix.mtx文件
        # if check_files_in_directory(file_path):
        #     print("loading adata object...")
        #     # 进行读取单细胞数据
        #     return sc.read_10x_mtx(
        #         path=file_path,  # the directory with the `.mtx` file
        #         var_names="gene_symbols",  # use gene symbols for the variable names (variables-axis index)
        #         cache=True,  # write a cache file for faster subsequent reading
        #     ), None


    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise FileExistsError(f"File is not exists: {file_path}")

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
