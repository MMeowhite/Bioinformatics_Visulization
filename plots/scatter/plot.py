import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

from utils.cluster import ClusterAlgorithm


class ScatterPlot:
    def __init__(self, args, data):
        self.args = args
        self.data = data

        if "X" not in data or "Y" not in data:
            raise ValueError("数据字典必须包含 'X' 和 'Y' 键")

        self.x = data["X"]
        self.y = data["Y"]

        if self.is_3d:
            if "Z" not in data:
                raise ValueError("If you want to plot 3d data, please specify the third dimension")
            self.z = data["Z"] if "Z" in data else None

        # 从 args 中获取参数，如果没有则使用默认值
        self.title = args.title if hasattr(self.args, 'title') else  'Multi Class Scatter Plot'
        self.xlab = args.xlab if hasattr(self.args, 'xlab') else 'X Axis Label'
        self.ylab = args.ylab if hasattr(self.args, 'ylab') else 'Y Axis Label'
        self.sizes = args.sizes if hasattr(args, 'sizes') else 100
        self.marker = args.marker if hasattr(args, 'markers') else 'o'
        self.categories = args.categories if hasattr(args, 'categories') else None


        self.bubble = args.bubble if hasattr(args, 'bubble') else None

        # category_colors 的逻辑需要根据 categories 是否存在来决定
        if self.categories is not None and hasattr(args, 'category_color'):
            self.category_colors = args.category_color
        else:
            self.category_colors = None

        self.colors = args.colors if hasattr(args, 'colors') else "blue"

        self.fig, self.ax = plt.subplots(figsize=(10, 8))

        # legend 的逻辑
        if hasattr(args, 'legend'):
            self.legend = args.legend
        else:
            self.legend = True

        self.legend_loc = args.legend_loc if hasattr(args, 'legend_loc') else 'upper right'

        # legend_position 的逻辑
        if hasattr(args, 'legend_position'):
            self.legend_position = args.legend_position
        else:
            self.legend_position = (1.05, 1)

        self.alpha = args.alpha if hasattr(args, 'alpha') else 0.8

        # 是否进行进一步的分析
        self.regression = args.regression if hasattr(args, 'regression') else False
        self.cluster = args.cluster if hasattr(args, 'cluster') else False
        self.method = args.method if hasattr(args, 'method') else "kmeans"
        self.number = args.number if hasattr(args, 'number') else 3

    def plot_scatter(self):
        # 普通散点图
        if self.categories is None:
            self.scatter = self.ax.scatter(self.x, self.y, s=self.sizes, alpha=self.alpha, marker=self.marker)
        else:
            if self.category_colors is None:
                unique_categories = np.unique(self.categories)
                category_colors = plt.cm.tab10(np.linspace(0, 1, len(unique_categories)))
                category_colors = {category: color for category, color in zip(unique_categories, category_colors)}
            self.colors = [self.category_colors[category] for category in self.categories]
            self.scatter = self.ax.scatter(self.x, self.y, s=self.sizes, alpha=self.alpha, marker=self.marker)
            if self.legend:
                category_handles = [
                    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=category_colors[category],
                               markersize=10, label=category)
                    for category in np.unique(self.categories)]
                self.ax.legend(handles=category_handles, title='Categories', loc=self.legend_loc, bbox_to_anchor=self.legend_position)

    def plot_bubble(self):
        # 气泡图
        if self.bubble_sizes is None:
            raise ValueError("气泡图需要提供 bubble_sizes 参数")
        scatter = self.ax.scatter(self.x, self.y, s=self.bubble_sizes, alpha=self.alpha, marker=self.marker)
        self.ax.set_title(self.title)
        self.ax.set_xlabel(self.xlab)
        self.ax.set_ylabel(self.ylab)

    def plot_3d(self):
        # 3D散点图
        if self.z is None:
            raise ValueError("3D散点图需要提供 z 参数")
        self.ax = self.fig.add_subplot(111, projection='3d')
        if self.categories is None:
            scatter = self.ax.scatter(self.x, self.y, self.z, s=self.sizes, alpha=self.alpha, marker=self.marker)
        else:
            if self.category_colors is None:
                unique_categories = np.unique(self.categories)
                category_colors = plt.cm.tab10(np.linspace(0, 1, len(unique_categories)))
                category_colors = {category: color for category, color in zip(unique_categories, category_colors)}
            colors = [self.category_colors[category] for category in self.categories]
            self.scatter = self.ax.scatter(self.x, self.y, self.z, c=colors, s=self.sizes, alpha=self.alpha, marker=self.marker)
            if self.legend:
                category_handles = [
                    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=self.category_colors[category],
                               markersize=10, label=category)
                    for category in np.unique(self.categories)]
                self.ax.legend(handles=category_handles, title='Categories', loc=self.legend_loc, bbox_to_anchor=self.legend_position)
        self.ax.set_title(self.title)
        self.ax.set_xlabel(self.xlab)
        self.ax.set_ylabel(self.ylab)
        self.ax.set_zlabel('Z Axis Label')

    def regression(self):
        # 绘制回归线
        if self.regression:
            slope, intercept, r_value, p_value, std_err = linregress(self.x, self.y)
            line_x = np.linspace(min(self.x), max(self.x), 100)
            line_y = slope * line_x + intercept
            self.ax.plot(line_x, line_y, color='gray', linestyle='--')
            equation_text = f'y = {slope:.2f}x + {intercept:.2f}'
            r_squared_text = f'R² = {r_value ** 2:.2f}'
            combined_text = f'{equation_text}\n{r_squared_text}'
            self.ax.text(0.01, 0.99, combined_text, transform=self.ax.transAxes, verticalalignment='top',
                    horizontalalignment='left', color='black', fontsize=12)


def plot(args, data, plot_type='scatter'):
    """
    绘制散点图函数，支持多种类型和功能。

    参数:
    args : 命令行参数对象
    data : 包含数据的字典，必须包含 "X" 和 "Y" 键
    title : 图表标题
    x_label : X轴标签
    y_label : Y轴标签
    categories : 数据类别列表
    sizes : 数据点大小
    z : Z轴数据，用于3D散点图
    category_colors : 类别对应的颜色
    legend : 是否显示图例
    legend_loc : 图例位置
    legend_position : 图例的精确位置
    regression : 是否绘制回归线
    plot_type : 散点图类型，可选值为 'scatter', 'bubble', '3d', 'matrix'
    bubble_sizes : 气泡大小数据，用于气泡图
    colormap : 颜色映射表
    grid : 是否显示网格
    alpha : 数据点的透明度
    marker : 数据点的标记样式
    """
    scatterPlot = ScatterPlot(args, data)

    # 根据plot_type选择绘制的散点图类型
    if plot_type == 'scatter':
        scatterPlot.plot_scatter()
    elif plot_type == 'bubble':
        scatterPlot.plot_bubble()
    elif plot_type == '3d':
        scatterPlot.plot_3d()
    else:
        raise ValueError("不支持的散点图类型")

    # 保存图像
    plt.savefig('scatter.png', dpi=300, bbox_inches='tight')


# 示例用法
if __name__ == "__main__":
    # 示例数据
    data = {
        "X": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "Y": [2, 3, 5, 7, 11, 13, 17, 19, 23],
        "categories": ['A', 'B', 'A', 'C', 'B', 'C', 'A', 'B', 'C'],
        "Z": [4, 5, 6, 7, 8, 9, 10, 11, 12],
        "bubble_sizes": [20, 30, 40, 50, 60, 70, 80, 90, 100]
    }

    # 调用绘图函数
    #plot(None, data, title='Example Scatter Plot', regression=True)
    #plot(None, data, title='Example Bubble Plot', plot_type='bubble', bubble_sizes=data["bubble_sizes"])
    plot(None, data, plot_type='3d')
    #plot(None, data, title='Example Matrix Scatter Plot', plot_type='matrix')