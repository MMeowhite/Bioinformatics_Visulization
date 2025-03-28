import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import linregress
import pandas as pd


class HistogramPlot:
    def __init__(self, args, data):
        self.args = args
        self.data = data
        self.fig, self.ax = plt.subplots(figsize=(10, 8))

        # 从 args 中获取参数，如果没有则使用默认值
        self.title = args.title if hasattr(args, 'title') else 'Histogram'
        self.xlab = args.xlab if hasattr(args, 'xlab') else 'xlabel'
        self.ylab = args.ylab if hasattr(args, 'ylab') else 'ylabel'

        self.ax.set_title(self.title)
        self.ax.set_xlabel(self.xlab)
        self.ax.set_ylabel(self.ylab)

        self.bins = args.bins if hasattr(args, 'bins') else 10
        self.alpha = args.alpha if hasattr(args, 'alpha') else 0.7
        self.color = args.color if hasattr(args, 'color') else 'blue'
        self.edgecolor = args.edgecolor if hasattr(args, 'edgecolor') else 'black'
        self.legend = args.legend if hasattr(args, 'legend') else False
        self.cumulative = args.cumulative if hasattr(args, 'cumulative') else False
        self.percentage = args.percentage if hasattr(args, 'percentage') else False
        self.kde = args.kde if hasattr(args, 'kde') else False

    def plot_simple(self):
        # 单变量直方图
        self.ax.hist(self.data,
                     bins=self.bins,
                     alpha=self.alpha,
                     color=self.color,
                     edgecolor=self.edgecolor
                     )


    def plot_overlaid(self):
        # 叠加直方图
        if not isinstance(self.data, list):
            raise ValueError("For overlaid histogram, data should be a list of datasets")
        colors = ['blue', 'green', 'red', 'purple', 'orange'][:len(self.data)]
        for i, d in enumerate(self.data):
            self.ax.hist(d, bins=self.bins, alpha=self.alpha, color=colors[i], edgecolor=self.edgecolor, label=f'Dataset {i+1}')
        if self.legend:
            self.ax.legend()


    def plot_cumulative(self):
        # 累积直方图
        self.ax.hist(self.data, bins=self.bins, alpha=self.alpha, color=self.color, edgecolor=self.edgecolor, cumulative=True)

    def plot_percentage(self):
        # 百分比直方图
        weights = np.ones_like(self.data) / len(self.data)
        self.ax.hist(self.data, bins=self.bins, weights=weights, alpha=self.alpha, color=self.color, edgecolor=self.edgecolor)


    def plot_2d(self):
        # 二维直方图
        if len(self.data) != 2:
            raise ValueError("For 2D histogram, data should be a list with two datasets")
        x, y = self.data
        heatmap, xedges, yedges = np.histogram2d(x, y, bins=self.bins)
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        self.ax.imshow(heatmap.T, extent=extent, origin='lower', cmap='viridis')
        plt.colorbar(self.ax.images[-1], ax=self.ax, label='Frequency')

    def plot_kde(self):
        # 核密度估计直方图
        sns.histplot(self.data, kde=self.kde, bins=self.bins, color=self.color)


    def plot_side_by_side(self):
        # 并排直方图
        if not isinstance(self.data, list):
            raise ValueError("For side-by-side histogram, data should be a list of datasets")
        colors = ['blue', 'green', 'red', 'purple', 'orange'][:len(self.data)]
        for i, d in enumerate(self.data):
            self.ax.hist(d, bins=self.bins, alpha=self.alpha, color=colors[i], edgecolor=self.edgecolor, label=f'Dataset {i+1}')
        if self.legend:
            self.ax.legend()



def plot(args, data, plot_type='simple'):
    """
    绘制直方图函数，支持多种类型。

    :parameter
        :param args : 命令行参数对象
        :param data : 数据，可以是单个数组或多维数组
        :param plot_type : 直方图类型，可选值为 'simple', 'overlaid', 'cumulative', 'percentage', '2d', 'kde', 'side_by_side'
    """
    hist_plot = HistogramPlot(args, data)

    if plot_type == 'simple':
        hist_plot.plot_simple()
    elif plot_type == 'overlaid':
        hist_plot.plot_overlaid()
    elif plot_type == 'cumulative':
        hist_plot.plot_cumulative()
    elif plot_type == 'percentage':
        hist_plot.plot_percentage()
    elif plot_type == '2d':
        hist_plot.plot_2d()
    elif plot_type == 'kde':
        hist_plot.plot_kde()
    elif plot_type == 'side_by_side':
        hist_plot.plot_side_by_side()
    else:
        raise ValueError("Unsupported histogram type")

    # 保存图像
    plt.savefig('histogram.png', dpi=300, bbox_inches='tight')


# 示例用法
if __name__ == "__main__":
    # 示例数据
    data_simple = pd.DataFrame(np.random.normal(0, 1, 1000))
    data_overlaid = [np.random.normal(0, 1, 1000), np.random.normal(2, 1, 1000)]
    data_2d = [np.random.normal(0, 1, 1000), np.random.normal(0, 1, 1000)]
    print(data_simple)

    # 绘制不同类型的直方图
    # plot(None, data_simple, plot_type='simple')
    plot(None, data_overlaid, plot_type='overlaid')
    # plot(None, data_simple, plot_type='cumulative')
    # plot(None, data_simple, plot_type='percentage')
    # plot(None, data_2d, plot_type='2d')
    # plot(None, data_simple, plot_type='kde')
    # plot(None, data_overlaid, plot_type='side_by_side')