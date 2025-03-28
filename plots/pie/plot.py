import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress


class PiePlot:
    def __init__(self, args, data):
        self.args = args
        self.data = data

        if "values" not in data or "labels" not in data:
            raise ValueError("数据字典必须包含 'values' 和 'labels' 键")

        self.values = data["values"]
        self.labels = data["labels"]

        # 从 args 中获取参数，如果没有则使用默认值
        self.title = args.title if hasattr(self.args, 'title') else 'Pie Plot'
        self.colors = args.colors if hasattr(self.args, 'colors') else None
        self.explode = args.explode if hasattr(self.args, 'explode') else None
        self.shadow = args.shadow if hasattr(self.args, 'shadow') else False
        self.startangle = args.startangle if hasattr(self.args, 'startangle') else 90
        self.legend = args.legend if hasattr(self.args, 'legend') else False
        self.legend_loc = args.legend_loc if hasattr(self.args, 'legend_loc') else 'upper right'
        self.legend_position = args.legend_position if hasattr(self.args, 'legend_position') else (1.05, 1)
        self.autopct = args.autopct if hasattr(self.args, 'autopct') else None
        self.pctdistance = args.pctdistance if hasattr(self.args, 'pctdistance') else 0.6
        self.labeldistance = args.labeldistance if hasattr(self.args, 'labeldistance') else 1.1
        self.textprops = args.textprops if hasattr(self.args, 'textprops') else None

        self.fig, self.ax = plt.subplots(figsize=(10, 8))

    def plot_basic_pie(self):
        # 普通饼状图
        wedges, texts, autotexts = self.ax.pie(
            self.values,
            explode=self.explode,
            labels=self.labels,
            colors=self.colors,
            shadow=self.shadow,
            startangle=self.startangle,
            autopct=self.autopct,
            pctdistance=self.pctdistance,
            labeldistance=self.labeldistance,
            textprops=self.textprops
        )

        # 设置文本属性
        for text in texts + autotexts:
            text.set_fontsize(10)
            text.set_color('black')

        # 添加图例
        if self.legend:
            self.ax.legend(
                wedges,
                self.labels,
                title="Categories",
                loc=self.legend_loc,
                bbox_to_anchor=self.legend_position
            )

        # 设置标题
        self.ax.set_title(self.title)

    def plot_doughnut(self):
        # 环形图
        wedges, texts, autotexts = self.ax.pie(
            self.values,
            explode=self.explode,
            labels=self.labels,
            colors=self.colors,
            shadow=self.shadow,
            startangle=self.startangle,
            autopct=self.autopct,
            pctdistance=self.pctdistance,
            labeldistance=self.labeldistance,
            textprops=self.textprops
        )

        # 添加中心圆
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        self.fig.gca().add_artist(centre_circle)

        # 设置文本属性
        for text in texts + autotexts:
            text.set_fontsize(10)
            text.set_color('black')

        # 添加图例
        if self.legend:
            self.ax.legend(
                wedges,
                self.labels,
                title="Categories",
                loc=self.legend_loc,
                bbox_to_anchor=self.legend_position
            )

        # 设置标题
        self.ax.set_title(self.title)

    def plot_3d_pie(self):
        # 3D饼状图
        from mpl_toolkits.mplot3d import Axes3D
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        # 绘制3D饼图
        wedges, texts, autotexts = ax.pie(
            self.values,
            explode=self.explode,
            labels=self.labels,
            colors=self.colors,
            shadow=self.shadow,
            startangle=self.startangle,
            autopct=self.autopct,
            pctdistance=self.pctdistance,
            labeldistance=self.labeldistance,
            textprops=self.textprops
        )

        # 设置文本属性
        for text in texts + autotexts:
            text.set_fontsize(10)
            text.set_color('black')

        # 添加图例
        if self.legend:
            ax.legend(
                wedges,
                self.labels,
                title="Categories",
                loc=self.legend_loc,
                bbox_to_anchor=self.legend_position
            )

        # 设置标题
        ax.set_title(self.title)

    def plot_grouped_pie(self):
        # 分组饼状图
        fig, axs = plt.subplots(1, len(self.values), figsize=(10, 8))
        for i, (group, values) in enumerate(zip(self.labels, self.values)):
            axs[i].pie(values, labels=self.labels, autopct='%1.1f%%', startangle=90)
            axs[i].set_title(group)
        plt.suptitle('Grouped Pie Chart')
        plt.savefig("demo.png", dpi=300)

    def plot_nested_pie(self):
        # 嵌套饼状图
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.axis('equal')

        # 外层饼图
        wedges, texts = ax.pie(self.values, labels=self.labels, radius=1, wedgeprops=dict(width=0.3, edgecolor='w'))

        # 内层饼图
        inner_wedges, inner_texts = ax.pie(self.values, radius=1 - 0.3, wedgeprops=dict(width=0.4, edgecolor='w'))

        plt.setp(inner_texts, size=8)
        plt.title('Nested Pie Chart')
        plt.savefig("demo.png", dpi=300)

    def plot_custom_percentage_pie(self):
        # 百分比自定义格式的饼状图
        def func(pct, allvals):
            absolute = int(np.round(pct / 100. * np.sum(allvals)))
            return f"{pct:.1f}%\n({absolute:d})"

        wedges, texts, autotexts = self.ax.pie(
            self.values,
            autopct=lambda pct: func(pct, self.values),
            textprops=dict(color="w"),
            startangle=self.startangle
        )

        plt.legend(wedges, self.labels, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.setp(autotexts, size=8, weight="bold")
        plt.title("Pie Chart with Custom Percentages")
        plt.axis('equal')
        plt.savefig("demo.png", dpi=300)


def plot(args, data, plot_type='basic'):
    """
    绘制饼图函数，支持多种类型和功能。

    参数:
    args : 命令行参数对象
    data : 包含数据的字典，必须包含 "values" 和 "labels" 键
    title : 图表标题
    colors : 扇形区域的颜色
    explode : 扇形区域的偏移量
    shadow : 是否添加阴影
    startangle : 起始角度
    legend : 是否显示图例
    legend_loc : 图例位置
    legend_position : 图例的精确位置
    autopct : 百分比格式字符串
    pctdistance : 百分比与圆心的距离
    labeldistance : 标签与圆心的距离
    textprops : 文本属性
    plot_type : 饼图类型，可选值为 'basic', 'doughnut', '3d', 'grouped', 'nested', 'custom_percentage', 'combined'
    """
    piePlot = PiePlot(args, data)

    # 根据plot_type选择绘制的饼图类型
    if plot_type == 'basic':
        piePlot.plot_basic_pie()
    elif plot_type == 'doughnut':
        piePlot.plot_doughnut()
    elif plot_type == '3d':
        piePlot.plot_3d_pie()
    elif plot_type == 'grouped':
        piePlot.plot_grouped_pie()
    elif plot_type == 'nested':
        piePlot.plot_nested_pie()
    elif plot_type == 'custom_percentage':
        piePlot.plot_custom_percentage_pie()
    else:
        raise ValueError("不支持的饼图类型")

    # 保存图像
    # plt.savefig('pie.png', dpi=300, bbox_inches='tight')


# 示例用法
if __name__ == "__main__":
    # 示例数据
    data = {
        "values": [30, 20, 50],
        "labels": ['A', 'B', 'C']
    }

    # 调用绘图函数
    # plot_pie(None, data, plot_type='basic')
    # plot_pie(None, data, plot_type='doughnut')
    # plot(None, data, plot_type='3d')
    plot(None, data, plot_type='grouped')
    # plot_pie(None, data, plot_type='nested')
    # plot_pie(None, data, plot_type='custom_percentage')
