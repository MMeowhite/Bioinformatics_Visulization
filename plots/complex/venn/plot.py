import matplotlib.pyplot as plt
from venn import venn
import pandas as pd


class VennPlot(object):
    def __init__(self, args, data):
        self.args = args
        self.data = self._pd_to_dict(data)
        self.color = args.color if 'color' in args else 'viridis'
        self.dpi = args.dpi if 'dpi' in args else 600

    def plot_venn(self):
        plt.figure(figsize=(6, 6))
        venn(self.data, cmap=self.color)
        plt.title("Venn Diagram for all Cities")
        plt.savefig('venn.png', dpi=self.dpi)

    def _pd_to_dict(self, data):
        if not isinstance(data, pd.DataFrame):
            raise TypeError(f'The data must be a DataFrame')
        result = {}
        for obs in data.columns:
            # 提取非空vars并转换为set
            vars = set(data[obs].dropna().unique().tolist())
            result[obs] = vars

        print(f"result: {result}")
        return result


def plot(args, data):
    venn_plot = VennPlot(args, data)
    venn_plot.plot_venn()


