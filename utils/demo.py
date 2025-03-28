import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, leaves_list
from scipy.spatial.distance import pdist

if __name__ == '__main__':
    # 示例数据
    np.random.seed(123)
    data = np.random.rand(20, 10)
    rownames = [f"Gene_{i + 1}" for i in range(20)]
    colnames = [f"Sample_{i + 1}" for i in range(10)]
    df = pd.DataFrame(data, index=rownames, columns=colnames)

    # 计算行和列的聚类
    # 行聚类
    row_dist = pdist(df, metric='euclidean')
    row_linkage = linkage(row_dist, method='ward')
    row_order = leaves_list(row_linkage)  # 提取叶节点的顺序
    print(f"row_order: {row_order}")

    # 列聚类
    col_dist = pdist(df.T, metric='euclidean')
    col_linkage = linkage(col_dist, method='ward')
    col_order = leaves_list(col_linkage)  # 提取叶节点的顺序
    print(f"col_order: {col_order}")

    # 重新排列数据框
    df_reordered = df.iloc[row_order, col_order]

    # 绘制聚类热图
    fig = plt.figure(figsize=(10, 8))

    # 创建子图布局
    gs = fig.add_gridspec(2, 2, width_ratios=[0.2, 1], height_ratios=[1, 0.2])

    # 左侧子图：行聚类树状图
    ax1 = fig.add_subplot(gs[0, 0])
    dendrogram(row_linkage, ax=ax1, orientation='left')
    ax1.axis('off')

    # 中间子图：热图
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.imshow(df_reordered, aspect='auto', cmap='viridis')
    ax2.set_yticks(np.arange(len(df_reordered.index)))
    ax2.set_yticklabels(df_reordered.index)
    ax2.set_xticks(np.arange(len(df_reordered.columns)))
    ax2.set_xticklabels(df_reordered.columns, rotation=90)

    # 下方子图：列聚类树状图
    ax3 = fig.add_subplot(gs[1, 1])
    dendrogram(col_linkage, ax=ax3, orientation='bottom')
    ax3.axis('off')

    plt.tight_layout()
    plt.savefig("demo.png")


