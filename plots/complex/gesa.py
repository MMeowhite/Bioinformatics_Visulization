import gseapy
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib import gridspec
from matplotlib.colors import ListedColormap


def gsea_plot(gsdata, geneSetID, title="", color="green", base_size=11, rel_heights=[1.5, 0.5, 1], subplots=[1, 2, 3], pvalue_table=False, ES_geom="line"):
    ES_geom = ES_geom.lower()
    if ES_geom not in ["line", "dot"]:
        raise ValueError("ES_geom must be 'line' or 'dot'")

    # Create a figure with subplots
    fig = plt.figure(figsize=(10, 8))
    gs = gridspec.GridSpec(len(rel_heights), 1, height_ratios=rel_heights)

    # First subplot: Running Enrichment Score
    ax1 = fig.add_subplot(gs[0])
    if ES_geom == "line":
        sns.lineplot(x="x", y="runningScore", hue="Description", data=gsdata, ax=ax1, palette=[color])
    else:
        sns.scatterplot(x="x", y="runningScore", hue="Description", data=gsdata[gsdata['position'] == 1], ax=ax1, palette=[color])
    ax1.set_ylabel("Running Enrichment Score")
    ax1.set_xlabel("")
    ax1.legend(loc='center right', title="", bbox_to_anchor=(1.2, 0.5))
    ax1.grid(True, axis='x', linestyle='--', color='grey')
    if title:
        ax1.set_title(title)

    # Second subplot: Gene Set Distribution
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    for term in gsdata['Description'].unique():
        subset = gsdata[gsdata['Description'] == term]
        ax2.hlines(y=0, xmin=subset['x'].min(), xmax=subset['x'].max(), color=color, linewidth=2)
    ax2.set_ylabel("")
    ax2.set_xlabel("")
    ax2.legend().remove()
    ax2.grid(False)

    # Third subplot: Ranked List Metric
    ax3 = fig.add_subplot(gs[2], sharex=ax1)
    sns.lineplot(x="x", y="geneList", data=gsdata, ax=ax3, color='grey')
    ax3.set_ylabel("Ranked List Metric")
    ax3.set_xlabel("Rank in Ordered Dataset")
    ax3.grid(False)

    # Adjust layout
    plt.tight_layout()

    # Show the plot
    plt.savefig("demo.png")

if __name__ == "__main__":
    # Example usage
    # Assuming gsdata is a pandas DataFrame with the required columns
    data = {
        'x': np.arange(1, 21),  # 基因排名
        'geneList': np.random.randn(20),  # 基因表达值或其他指标
        'runningScore': np.random.randn(20),  # 累积富集得分
        'Description': ['Gene_Set_A'] * 10 + ['Gene_Set_B'] * 10,  # 基因集描述
        'position': [1] * 5 + [0] * 15  # 是否在基因集中的位置标记
    }


    gsdata = pd.DataFrame(data)
    gsea_plot(gsdata, geneSetID="example_set", title="GSEA Analysis", color="green")