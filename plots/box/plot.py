import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.decorator import log


def plot_boxplot(args, data, **kwargs):
    """
    主函数，用于绘制箱线图。

    parameters:
    - args: 包含分析参数的命名空间，如输出目录、标题等。
    - data: 输入数据，可以是 Pandas DataFrame 或字典。
    - kwargs: 其他关键字参数，如 x 轴标签、y 轴标签等。
    """
    # 提取参数
    x_label = kwargs.get('x_label', 'X-axis')
    y_label = kwargs.get('y_label', 'Y-axis')
    title = kwargs.get('title', 'Box Plot')
    outdir = kwargs.get('outdir', 'boxplot_results')

    # 确保输出目录存在
    os.makedirs(outdir, exist_ok=True)

    # 绘制箱线图
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data)

    # 设置图表标题和轴标签
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # 保存图表
    plt.savefig(f"{outdir}/boxplot.png", dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    import argparse

    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description='箱线图绘制工具')
    parser.add_argument('--data', type=str, required=True, help='输入数据文件')
    parser.add_argument('--outdir', type=str, default='boxplot_results', help='输出目录')
    parser.add_argument('--title', type=str, default='Box Plot', help='图表标题')
    parser.add_argument('--x_label', type=str, default='X-axis', help='X 轴标签')
    parser.add_argument('--y_label', type=str, default='Y-axis', help='Y 轴标签')

    args = parser.parse_args()

    # 读取数据
    data = pd.read_csv(args.data)

    # 绘制箱线图
    plot_boxplot(args, data, x_label=args.x_label, y_label=args.y_label, title=args.title)