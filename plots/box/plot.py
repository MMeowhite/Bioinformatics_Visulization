import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.decorator import log
import os


class BoxPlot():
    def __init__(self, args, data):
        self.args = args
        self.data = data
        self.fig, self.ax = plt.subplots()
        self.x_labels, self.y_labels = [], []

    def plot_simple(self):


def plot(args, data, **kwargs):
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

