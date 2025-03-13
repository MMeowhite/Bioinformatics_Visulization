import argparse
import sys
import os
import csv
import pandas as pd
from plots.plot_dispatcher import dispatch_plot

def get_file_type(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower()

def load_data_from_file(file_path):
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
    
    # 加载数据
    data = {}
    try:
        if file_extension in ['.csv', '.txt']:
            # 读取 CSV 或 TXT 文件
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                headers = next(reader)  # 读取表头
                # 初始化数据字典
                for header in headers:
                    data[header] = []
                # 读取数据行
                for row in reader:
                    if len(row) == len(headers):
                        for i, header in enumerate(headers):
                            try:
                                # 尝试将数值列转换为浮点数，非数值列保持为字符串
                                value = float(row[i])
                            except ValueError:
                                value = row[i]
                            data[header].append(value)
        elif file_extension in ['.xls', '.xlsx']:
            # 读取 Excel 文件
            df = pd.read_excel(file_path)
            # 获取列名
            headers = df.columns.tolist()
            # 初始化数据字典
            for header in headers:
                data[header] = []
            # 读取数据
            for _, row in df.iterrows():
                for header in headers:
                    value = row[header]
                    try:
                        # 尝试将数值列转换为浮点数，非数值列保持为字符串
                        value = float(value)
                    except ValueError:
                        pass
                    data[header].append(value)
        
        return data
    except Exception as e:
        print(f"Error loading data from file: {e}")
        sys.exit(1)

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Plotting Tool")
    parser.add_argument("-t", "--type", required=True, help="Type of plot (e.g., line, bar, scatter, hist)")
    parser.add_argument("-f", "--file", help="Path to the data file (csv, xlsx, xls format)")
    parser.add_argument("--color", help="Color of the plot")
    parser.add_argument("--linestyle", help="Line style for line plot")
    parser.add_argument("--marker", help="Marker style for scatter plot")
    parser.add_argument("--bins", type=int, help="Number of bins for histogram")
    args = parser.parse_args()
    print(f"args:{args}")

    # 加载数据
    data = None
    if args.file:
        try:
            data = load_data_from_file(args.file)
        except Exception as e:
            print(e)
            sys.exit(1)
    else:
        # 使用默认数据
        data = {'x': [1, 2, 3, 4, 5], 'y': [10, 20, 25, 30, 40]}

    # 准备可选参数
    kwargs = {}
    if args.color:
        kwargs["color"] = args.color
    if args.linestyle:
        kwargs["linestyle"] = args.linestyle
    if args.marker:
        kwargs["marker"] = args.marker
    if args.bins:
        kwargs["bins"] = args.bins

    try:
        dispatch_plot(args.type, data)
    except ValueError as e:
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()