import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class ViolinPlot:
    def __init__(self, args, data):
        self.args = args
        self.data = data

    def violin_simple(self):
        # 检查数据是否为空
        if self.data is None or self.data.empty:
            raise ValueError("数据为空，请提供有效的数据。")

        # 检查数据是否为 Pandas DataFrame
        if not isinstance(self.data, pd.DataFrame):
            raise TypeError("数据必须是 Pandas DataFrame 类型。")

        # 检查绘图参数
        title = self.args.get("title", "Gene Expression Distribution")
        xlabel = self.args.get("xlabel", "Genes")
        ylabel = self.args.get("ylabel", "Expression Values")
        figsize = self.args.get("figsize", (10, 6))
        save_path = self.args.get("save_path", None)
        show_points = self.args.get("show_points", False)  # 是否显示点的分布
        dpi = self.args.get("dpi", 300)

        # 创建小提琴图
        plt.figure(figsize=figsize)
        ax = sns.violinplot(data=self.data)

        # 如果需要显示点的分布，添加 stripplot
        if show_points:
            sns.stripplot(data=self.data, color="black", size=3, jitter=True, ax=ax)

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        # 保存或显示图表
        if save_path:
            plt.savefig(save_path, dpi=dpi)
            print(f"图表已保存到: {save_path}")



def plot(args, data):
    violin = ViolinPlot(args, data)
    violin.violin_simple()



# 示例数据
def generate_example_data():
    np.random.seed(42)
    data = {
        "Gene1": np.random.randint(0, 100, 100),
        "Gene2": np.random.randint(0, 100, 100),
        "Gene3": np.random.randint(0, 100, 100),
        "Gene4": np.random.randint(0, 100, 100)
    }
    return pd.DataFrame(data)


if __name__ == "__main__":
    # 生成示例数据
    df = generate_example_data()

    # 绘图参数
    args = {
        "title": "Gene Expression Distribution",
        "xlabel": "Genes",
        "ylabel": "Expression Values",
        "figsize": (10, 6),
        "save_path": "violin_plot.png",  # 如果不需要保存，可以设置为 None
        "show_points": True,  # 是否显示点的分布
        "dpi": 600
    }

    # 调用 plot 函数生成小提琴图
    plot(args, df)