import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
from utils.decorator import log


class ScatterPlot:
    def __init__(self, args, data):
        self.args = args
        self.data = data
        self.x = data["X"]
        self.y = data["Y"]
        self.z = data["Z"] if "Z" in data.keys() else None
        self.sizes = data["sizes"] if "sizes" in data else 100
        self.markers = data["markers"] if "markers" in data.keys() else 'o'
        self.categories = args.categories if "categories" in args else None
        self.category_colors = args.category_color if args.categories is not None else None
        self.colors = args.colors if args.colors is not None else "blue"
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.legend = args.legend if args.legend is not None else True
        self.legend_loc = args.legend_loc
        self.legend_position = args.legend_position if args.legend_position is not None else (1.05, 1)
        self.regression = args.regression if args.regression is not None else False


    def plot_scatter(self):
        # 普通散点图
        if self.categories is None:
            scatter = self.ax.scatter(self.x, self.y, s=self.sizes, alpha=self.alpha, marker=self.marker)
        else:
            if self.category_colors is None:
                unique_categories = np.unique(self.categories)
                category_colors = plt.cm.tab10(np.linspace(0, 1, len(unique_categories)))
                category_colors = {category: color for category, color in zip(unique_categories, category_colors)}
            colors = [self.category_colors[category] for category in self.categories]
            scatter = self.ax.scatter(self.x, self.y, s=self.sizes, alpha=self.alpha, marker=self.marker)
            if self.legend:
                category_handles = [
                    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=category_colors[category],
                               markersize=10, label=category)
                    for category in np.unique(self.categories)]
                self.ax.legend(handles=category_handles, title='Categories', loc=self.legend_loc, bbox_to_anchor=self.legend_position)


def plot(args, data, title='Multi Class Scatter Plot', x_label='X Axis Label',
         y_label='Y Axis Label', categories=None, sizes=100, z=None,
         category_colors=None, legend=True, legend_loc='upper right',
         legend_position=(1.05, 1), regression=False, plot_type='scatter',
         bubble_sizes=None, colormap='viridis', grid=False, alpha=0.8,
         marker='o'):
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

    # 参数验证
    if "X" not in data or "Y" not in data:
        raise ValueError("数据字典必须包含 'X' 和 'Y' 键")

    x = np.array(data["X"])
    y = np.array(data["Y"])



    # 根据plot_type选择绘制的散点图类型
    if plot_type == 'scatter':
        scatterPlot.plot_scatter()

    elif plot_type == 'bubble':
        # 气泡图
        if bubble_sizes is None:
            raise ValueError("气泡图需要提供 bubble_sizes 参数")
        scatter = ax.scatter(x, y, s=bubble_sizes, alpha=alpha, marker=marker)
        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

    elif plot_type == '3d':
        # 3D散点图
        if z is None:
            raise ValueError("3D散点图需要提供 z 参数")
        ax = fig.add_subplot(111, projection='3d')
        if categories is None:
            scatter = ax.scatter(x, y, z, s=sizes, alpha=alpha, marker=marker)
        else:
            if category_colors is None:
                unique_categories = np.unique(categories)
                category_colors = plt.cm.tab10(np.linspace(0, 1, len(unique_categories)))
                category_colors = {category: color for category, color in zip(unique_categories, category_colors)}
            colors = [category_colors[category] for category in categories]
            scatter = ax.scatter(x, y, z, c=colors, s=sizes, alpha=alpha, marker=marker)
            if legend:
                category_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=category_colors[category], markersize=10, label=category)
                                    for category in np.unique(categories)]
                ax.legend(handles=category_handles, title='Categories', loc=legend_loc, bbox_to_anchor=legend_position)
        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_zlabel('Z Axis Label')

    elif plot_type == 'matrix':
        # 矩阵散点图
        if len(data) < 3:
            raise ValueError("矩阵散点图需要至少三个变量")
        df = pd.DataFrame(data)
        pd.plotting.scatter_matrix(df, figsize=(10, 10), diagonal='kde')
        plt.suptitle(title)

    else:
        raise ValueError("不支持的散点图类型")

    # 绘制回归线
    if regression and plot_type in ['scatter', 'bubble']:
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        line_x = np.linspace(min(x), max(x), 100)
        line_y = slope * line_x + intercept
        ax.plot(line_x, line_y, color='gray', linestyle='--')
        equation_text = f'y = {slope:.2f}x + {intercept:.2f}'
        r_squared_text = f'R² = {r_value**2:.2f}'
        combined_text = f'{equation_text}\n{r_squared_text}'
        ax.text(0.01, 0.99, combined_text, transform=ax.transAxes, verticalalignment='top', horizontalalignment='left', color='black', fontsize=12)

    # 显示网格
    if grid:
        ax.grid(True)

    # 保存图像
    plt.savefig('scatter.png', dpi=300, bbox_inches='tight')

    # 显示图像
    plt.show()

    # 关闭图像
    plt.close()

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
    plot(None, data, title='Example 3D Scatter Plot', plot_type='3d', z=data["Z"])
    #plot(None, data, title='Example Matrix Scatter Plot', plot_type='matrix')