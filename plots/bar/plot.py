import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class BarPlot:
    def __init__(self, data, **kwargs):
        self.data = data
        # setting default param
        self.xlabel = kwargs.get('xlabel', 'xlabel')
        self.ylabel = kwargs.get('ylabel', 'ylabel')
        self.title = kwargs.get('title', 'title')
        self.dpi = kwargs.get('dpi', 300)
        self.filename = kwargs.get('filename', 'bar_chart.png')
        self.color = kwargs.get('color', ["blue", "green", "red"])
        # 差值条形图
        self.baseline = kwargs.get('baseline', 0)

    def plot_simple(self):
        # simple bar
        plt.bar(self.data['Group'], self.data['Category1'], label='Category1', color='blue')
        plt.bar(self.data['Group'], self.data['Category2'], label='Category2', color='green')
        plt.bar(self.data['Group'], self.data['Category3'], label='Category3', color='red')

        plt.savefig(self.filename, dpi=self.dpi, bbox_inches='tight')


    def plot_stacked(self):
        # stacked bar
        x = np.arange(len(self.data['Group']))
        width = 0.7
        plt.bar(x, self.data['Category1'], width, label='Category1', color='blue')
        plt.bar(x, self.data['Category2'], width, label='Category2', bottom=self.data['Category1'], color='green')
        plt.bar(x, self.data['Category3'], width, label='Category3', bottom=self.data['Category1'] + data['Category2'],
                color='red')
        plt.xticks(x, data['Group'])

        plt.savefig(self.filename, dpi=self.dpi, bbox_inches='tight')

    def plot_grouped(self):
        # grouped bar
        x = np.arange(len(self.data['Group']))
        width = 0.2
        plt.bar(x - width, self.data['Category1'], width, label='Category1', color='blue')
        plt.bar(x, self.data['Category2'], width, label='Category2', color='green')
        plt.bar(x + width, self.data['Category3'], width, label='Category3', color='red')
        plt.xticks(x, self.data['Group'])

        plt.savefig(self.filename, dpi=self.dpi, bbox_inches='tight')

    def plot_horizontal(self):
        # horizontal bar
        plt.barh(self.data['Group'], self.data['Category1'], label='Category1', color='blue')
        plt.barh(self.data['Group'], self.data['Category2'], label='Category2', color='green')
        plt.barh(self.data['Group'], self.data['Category3'], label='Category3', color='red')

        plt.savefig(self.filename, dpi=self.dpi, bbox_inches='tight')

    def plot_deviation(self):

        deviations1 = self.data['Category1'] - baseline
        deviations2 = data['Category2'] - baseline
        deviations3 = data['Category3'] - baseline
        plt.bar(data['Group'], deviations1, label='Category1', color='blue')
        plt.bar(data['Group'], deviations2, label='Category2', color='green')
        plt.bar(data['Group'], deviations3, label='Category3', color='red')
        plt.axhline(y=0, color='black', linestyle='--')

        plt.savefig(self.filename, dpi=self.dpi, bbox_inches='tight')

    def plot_percentage(self):
        # 百分比条形图
        total = self.data['Category1'] + self.data['Category2'] + self.dataa['Category3']
        percentages1 = (self.data['Category1'] / total) * 100
        percentages2 = (self.data['Category2'] / total) * 100
        percentages3 = (self.data['Category3'] / total) * 100
        plt.bar(self.data['Group'], percentages1, label='Category1', color='blue')
        plt.bar(self.data['Group'], percentages2, label='Category2', color='green', bottom=percentages1)
        plt.bar(self.data['Group'], percentages3, label='Category3', color='red', bottom=percentages1 + percentages2)

        plt.savefig(self.filename, dpi=self.dpi, bbox_inches='tight')

    def plot_segmented(self):
        # 分段条形图
        x = np.arange(len(self.data['Group']))
        width = 0.7
        plt.bar(x, self.data['Category1'], width, label='Category1', color='blue')
        plt.bar(x, self.data['Category2'], width, label='Category2', bottom=self.data['Category1'], color='green')
        plt.bar(x, self.data['Category3'], width, label='Category3', bottom=self.data['Category1'] + self.data['Category2'],
                color='red')
        plt.xticks(x, self.data['Group'])

        plt.savefig(self.filename, dpi=self.dpi, bbox_inches='tight')

    def plot_bar_line(self):
        # 条形图与线图结合
        plt.bar(self.data['Group'], self.data['Category1'], label='Category1', color='blue')
        plt.plot(self.data['Group'], self.data['Category2'], marker='o', color='red', label='Category2')
        plt.plot(self.data['Group'], self.data['Category3'], marker='s', color='green', label='Category3')

        plt.savefig(self.filename, dpi=self.dpi, bbox_inches='tight')


def plot(data, **kwargs):
    """
    plot bar chart

    :parameter:
    :param data : pd.DataFrame
        DataFrame containing the data
    :param **kwargs : optional param
        - xlabel : x-axis label
        - ylabel : y-axis label
        - title : chart title
        - dpi :  resolution, default: 300dpi
        - filename : file name
    """
    barPlot = BarPlot(data, **kwargs)

    print(f"data: {data}")


    if kwargs["class"] == 'simple':
        barPlot.plot_simple()

    elif kwargs["class"] == 'stacked':
        barPlot.plot_stacked()

    elif kwargs["class"] == 'grouped':
        barPlot.plot_grouped()

    elif kwargs["class"] == 'horizontal':
        barPlot.plot_horizontal()

    elif kwargs["class"] == 'deviation':
        barPlot.plot_deviation()

    elif kwargs["class"] == 'percentage':
        barPlot.plot_percentage()

    elif kwargs["class"] == 'segmented':
        barPlot.plot_segmented()

    elif kwargs["class"] == 'bar_line':
        barPlot.plot_bar_line()

    else:
        raise ValueError("Invalid chart type. Supported types are: 'simple', "
                         "'stacked', 'grouped', 'horizontal', 'deviation', "
                         "'percentage', 'segmented', 'bar_line'")

    # add legend
    plt.legend()


if __name__ == '__main__':

    # 示例数据
    data = {
        'Group': ['A', 'B', 'C', 'D'],
        'Category1': [10, 15, 12, 18],
        'Category2': [5, 8, 6, 11],
        'Category3': [3, 4, 2, 7]
    }

    df = pd.DataFrame(data)

    # 绘制不同类型的条形图
    # plot(df, chart_type='simple', xlabel='Group', ylabel='Values', title='Simple Bar Chart', filename='simple_bar.png')
    # plot(df, chart_type='stacked', xlabel='Group', ylabel='Values', title='Stacked Bar Chart', filename='stacked_bar.png')
    # plot(df, chart_type='grouped', xlabel='Group', ylabel='Values', title='Grouped Bar Chart', filename='grouped_bar.png')
    # plot(df, chart_type='horizontal', xlabel='Values', ylabel='Group', title='Horizontal Bar Chart', filename='horizontal_bar.png')
    # plot(df, chart_type='deviation', xlabel='Group', ylabel='Deviation', title='Deviation Bar Chart', filename='deviation_bar.png')
    # plot(df, chart_type='percentage', xlabel='Group', ylabel='Percentage', title='Percentage Bar Chart', filename='percentage_bar.png')
    plot(df, xlabel='Group', ylabel='Values', title='Segmented Bar Chart', filename='segmented_bar.png')
    # plot(df, chart_type='bar_line', xlabel='Group', ylabel='Values', title='Bar and Line Chart', filename='bar_line.png')